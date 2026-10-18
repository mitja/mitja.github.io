---
title: "A Local Cloud Lab on Apple's Virtualization.framework: Hot-Plug Disks, a 200-Line Switch, and Four Ways to Attach a Volume"
summary: "I wanted to replace Parallels Desktop in my Hetzner Cloud API mockup with Apple's built-in hypervisor, driven from Go. Booting VMs was easy. Letting two VMs talk to each other took a small userspace switch, and attaching volumes to running VMs led to a benchmark of USB disk images, iSCSI, NVMe/TCP and plain virtio."
date: 2026-09-15
draft: true
categories:
  - Platform Engineering
tags:
  - macOS
  - Virtualization.framework
  - Go
  - Storage
  - NVMe/TCP
  - iSCSI
  - Kubernetes
showHero: false
---

I have been building ownpaas, a mockup of the Hetzner Cloud API that runs real VMs. The `hcloud` CLI, Terraform, Packer and hetzner-k3s all talk to it as if it were Hetzner. On a Kubernetes cluster it runs KubeVirt VMs. On my Mac it has so far used Parallels Desktop, and recently hetzner-k3s built a three-node cluster on Parallels VMs through it, with the hcloud cloud controller manager and CSI driver working against the mockup.

Parallels works, but it is a commercial app with a GUI that sometimes asks questions nobody is there to answer. macOS ships a hypervisor API, Virtualization.framework, and [Code-Hex/vz](https://github.com/Code-Hex/vz) makes it usable from Go. So the question was whether a Go driver on the built-in framework can do everything the Parallels driver does. That means booting cloud images with cloud-init, attaching volumes to running VMs, letting VMs talk to each other, and doing all of it well enough for a Kubernetes cluster.

This post is the result of a spike. The short version:

- Booting works, with two gotchas around cloud-init and DHCP.
- USB disk images can be attached to running VMs, and fast, but they are anonymous and never flush.
- VMs on the built-in NAT network cannot reach each other at all. A userspace Ethernet switch of about 200 lines of Go fixes that, at up to 5.4 Gbit/s.
- With that switch, a storage appliance VM can serve volumes over iSCSI or NVMe/TCP. NVMe/TCP needs nothing installed in the guest.

All code is at the end of the post and next to it as files. It is spike code, not production code.

## Setup

- Mac Studio with M3 Ultra, 256 GB, macOS 26.5.1
- Go 1.26, `github.com/Code-Hex/vz/v3` v3.7.1
- Guests: the Debian 13 `generic` arm64 cloud image, as a raw file

The runner, `vzprobe`, starts one VM per process and takes commands on a localhost TCP port: attach or detach a USB disk, attach an NBD export, stop. One process per VM is not an accident. A VM lives inside the process that created it, so a management API that restarts must not own the VMs itself.

The binary needs one entitlement, `com.apple.security.virtualization`, and an ad-hoc signature is enough:

```sh
go build -o vzprobe . && codesign --entitlements vz.entitlements -s - -f vzprobe
```

No Apple developer account is involved. Bridged networking would need a restricted entitlement, but NAT does not.

## Booting: two cloud-init surprises

The root disk is an APFS clone of the raw image (`cp -c`, instant), grown with `truncate`. It boots through `VZEFIBootLoader` with a generic platform, a virtio disk, a virtio NIC on NAT, and the serial console written to a file.

**The seed must be a FAT disk.** Parallels takes a NoCloud ISO as a virtual CD-ROM, and cloud-init reads it. The same ISO attached as a read-only virtio disk was ignored: the VM came up as `localhost` with no SSH keys. A 4 MB FAT12 image labeled `CIDATA` works. `hdiutil` can build one, and `dd` from the raw device turns it into a plain file (see `make-vm.sh`).

**The macOS DHCP server keys leases by DUID.** `/var/db/dhcpd_leases` shows `hw_address=ff,f1:f5:dd:…` for a fresh Debian guest, so the address cannot be looked up by MAC. With `dhcp-identifier: mac` in the network-config, the lease reads `hw_address=1,52:54:0:a:0:1`. For a cloud mockup I would rather allocate addresses myself anyway and set them statically, so that the create call can return the IP as Hetzner's does.

## Hot-plugging disks: USB is the only way, and it is anonymous

Virtio block devices are fixed when the VM starts. Since macOS 15 there is one device class that can be attached at runtime: USB mass storage on an XHCI controller, backed by a disk image or an NBD export.

```go
dc, _ := vz.NewUSBMassStorageDeviceConfiguration(attachment)
dev, _ := vz.NewUSBMassStorageDevice(dc)
err := vm.USBControllers()[0].Attach(dev)
```

It works well mechanically. Attach takes about 7 ms and detach under 1 ms, the guest sees the disk immediately, and data survives a detach and reattach. The limits are these:

- **No identity.** Every disk reports vendor `Apple`, model `Virtual Disk`, serial `Apple_Virtual_Disk-0:0`. The only distinguishing property is the USB port in `/dev/disk/by-path`. The controller always picks the lowest free port, so a management plane can track port-to-volume assignments, but the guest needs that table from somewhere, such as the metadata service.
- **Eight disks per VM.** The ninth attach fails with `VZErrorDomain Code=30003`.
- **No flushes.** The guest reports the disk as `write through`, so Linux never sends SYNCHRONIZE CACHE. That explains the benchmark below, where an fsync-heavy workload on USB is 10 to 20 times faster than on virtio. It also means the writes rely on host buffering for durability.

For comparison, Parallels lets you name the disk file, and the file name shows up as the ATA model, so a udev rule can derive `/dev/disk/by-id/scsi-0HC_Volume_<id>` as on Hetzner. Here that trick is not available.

## VMs cannot talk to each other

The first storage appliance test failed with `No route to host`: iSCSI from one VM to another. The guest's ARP entry for the other VM stayed `INCOMPLETE`. The reason is on the host:

```text
bridge102: flags=8a63<UP,BROADCAST,SMART,RUNNING,ALLMULTI,SIMPLEX,MULTICAST> mtu 1500
	member: vmenet6 flags=20803<LEARNING,DISCOVER,PRIVATE,VIRTIO>
	member: vmenet7 flags=20803<LEARNING,DISCOVER,PRIVATE,VIRTIO>
```

Every VM's port on the NAT bridge is `PRIVATE`: VMs reach the Mac and the internet, but not each other. For a laptop running one Linux VM that is a sensible default. For a cloud lab it rules out Kubernetes nodes talking to each other, storage traffic, and load balancers in a VM reaching their backends.

Unsetting the flag needs root and would have to be repeated for every new `vmenet` interface. Tools like Lima solve it with `socket_vmnet`, a root daemon. I wanted neither.

## A switch in 200 lines

Virtualization.framework has a third network attachment besides NAT and bridged: `VZFileHandleNetworkDeviceAttachment`, a datagram socket where each datagram is one Ethernet frame. The `vz` binding checks only that the socket is `SOCK_DGRAM` with an inet or unix address. That means a UDP socket works, which avoids the 104-character limit on unix socket paths and any relay process.

Each VM gets a second NIC:

1. `vzprobe` creates a UDP socket, binds it to a fixed local port such as `127.0.0.1:17101`, connects it to the switch at `127.0.0.1:17100`, and hands the file descriptor to the framework.
2. `vzswitch` reads frames, learns source MACs per network, forwards known unicast, and floods broadcast and unknown unicast within the network.
3. A switch port is the VM's UDP source port, and each port belongs to a network ID. The guest cannot choose its port, so it cannot choose its network either. That is the basis for isolated private networks.

| test | result |
|---|---|
| ping between VMs | 0.5 ms, no loss |
| iperf3, MTU 1500 | ~1 Gbit/s |
| iperf3, MTU 9000 (`SetMaximumTransmissionUnit`) | 5.4 Gbit/s, 5.2 Gbit/s with four streams |
| move a port to another network at runtime | traffic stops immediately; moving it back restores it |
| guest takes another VM's MAC | nothing gets through, but it poisons the MAC table within its own network |
| frames | about 2.3 million forwarded, 0 drops |

A real version pins one MAC per port. The single-threaded forwarding loop is the obvious next thing to measure, since MTU 9000 already moves the bottleneck from the frame count to the copy.

## Four ways to attach a volume

With VMs able to reach each other, a storage appliance becomes possible: one VM that owns the volumes and exports them to the servers. I tried three variants against a USB disk image and a cold-attached virtio disk as the reference:

| path | how | hot-plug | identity in the guest | guest needs |
|---|---|---|---|---|
| **virtio** (reference) | raw file on the Mac, attached at boot | no | none by default (`SetBlockDeviceIdentifier` exists) | nothing |
| **USB** | raw file on the Mac, `USBController.Attach` | yes | none (USB port only) | a port-to-volume table |
| **iSCSI** | LIO in the appliance, block backstore on an LV | yes, LUN add plus rescan | model from the backstore name (16 characters max), serial settable before export | `open-iscsi`, a rescan trigger |
| **NVMe/TCP** | `nvmet` in the appliance, one subsystem per volume | yes, connect per volume | model and serial free-form: `/dev/disk/by-id/nvme-HC_Volume_302_…` | nothing: `nvme-tcp` is in the Debian kernel |

I also attached an appliance's `qemu-nbd` export as a USB disk through the framework's built-in NBD client: attach took 47 ms, and data written in the client VM landed in the appliance's file. It combines hypervisor-side attach with network storage, but inherits USB's anonymity.

Two details decided more than the numbers did:

- **iSCSI does not announce new LUNs.** After adding a LUN to a logged-in session, the guest saw nothing until `iscsiadm -m session -R`. A guest agent can run that, but it is one more moving part.
- **NVMe/TCP needs no userspace at all.** On a stock Debian 13 cloud image, with `nvme-cli` removed:

  ```sh
  echo "transport=tcp,traddr=10.99.0.2,trsvcid=4420,nqn=hc-volume-302" > /dev/nvme-fabrics
  # ... /dev/nvme0n1, model and serial HC_Volume_302
  echo 1 > /sys/class/nvme/nvme0/delete_controller
  ```

  On the appliance side it is plain configfs, with no `targetcli`.

## Benchmark

`fio` on each device from the same client VM (4 vCPU, 4 GB): 20 seconds per job, direct I/O, `libaio`. Last comes the common etcd disk check: sequential 2300-byte writes with `fdatasync` on ext4. The appliance has 4 vCPU and 4 GB, and its LVs sit on its own virtio data disk, a raw file on the Mac. The switch NICs use MTU 9000. Each test ran once, so treat differences under about 20 % as noise.

| metric | virtio | USB | iSCSI | NVMe/TCP |
|---|---|---|---|---|
| 4k random read, qd32, IOPS | 136,889 | 6,308 | 39,240 | 41,938 |
| 4k random write, qd32, IOPS | 14,238 | 4,897 | 12,100 | 14,045 |
| 4k random 70/30, qd16 × 2 jobs, IOPS | 32,243 | 4,978 | 27,272 | 30,039 |
| 4k random write, qd1, IOPS | 11,713 | 4,923 | 3,059 | 3,942 |
| 4k random write, qd1, p99 (ms) | 0.15 | 0.36 | 0.56 | 0.45 |
| 1M sequential write, MB/s | 1,126 | 1,448 | 248 | 233 |
| 1M sequential read, MB/s | 1,135 | 936 | 582 | 567 |
| etcd fdatasync p50 (ms) | 9.63 | 0.52 | 6.13 | 10.55 |
| etcd fdatasync p99 (ms) | 13.04 | 1.02 | 8.59 | 13.04 |
| etcd writes/s | 121 | 2,050 | 158 | 113 |

How I read it:

- **virtio is the ceiling,** but it cannot be attached to a running VM. It remains the right choice for root disks and for volumes present at boot.
- **USB is fast for streaming and weak for parallel random I/O.** The guest uses the old `usb-storage` bulk-only driver with a single command queue. Random IOPS barely change between queue depth 1 and 32. Its etcd numbers are not a feature: the guest never flushes.
- **The network paths keep most of the random I/O,** at three to eight times USB under parallel load. They lose at queue depth 1 and on sequential throughput, which is where the switch's copies show. iSCSI and NVMe/TCP are within noise of each other.
- **About 10 ms fsync on virtio** is the price of real flushes to the Mac's SSD. The network paths inherit it from the appliance's virtio disk. etcd accepts it, but it rules out a tight latency budget.

## What I am building

The ownpaas driver for Virtualization.framework was meant to look like this (see the update below for how it turned out):

- **One helper process per VM,** as in the spike, so the API server can restart without taking servers down.
- **Two NICs per VM.** The NAT NIC carries the server's public address (allocated by ownpaas, set statically), SSH from the Mac, health checks and the metadata service. The switch NIC carries VM-to-VM traffic and Hetzner private networks, one switch network per network.
- **Volumes on a storage appliance over NVMe/TCP,** with a small guest service that connects and disconnects exports as the metadata service lists them. It needs nothing installed in the guest, a udev rule links `scsi-0HC_Volume_<id>` for tools that expect Hetzner's path, and it keeps most of the random I/O. A USB disk image stays as the zero-appliance fallback, where the data is a plain file you can copy.
- **hetzner-k3s with private networks enabled,** so node traffic and flannel use the switch rather than the isolated NAT network.

If you only need one or two Linux VMs on a Mac, none of this is necessary: the NAT network and virtio disks are fast and simple. The complexity starts with the second VM that needs to reach the first.

## Update: the driver exists now

I built the driver the same day, and hetzner-k3s now runs on it: one master and two workers, a private network, the hcloud cloud controller manager and the CSI driver.

- **Nodes** get their provider IDs, zones and private IPs.
- **A `LoadBalancer` Service** becomes HAProxy in the storage appliance, and traffic flows from the Mac to the pod.
- **A PVC** is provisioned as an NVMe/TCP volume. When I drained its node, it moved to another worker in 24 seconds with its data.

The design survived contact with reality, but the details did not. These are the problems I ran into, because each of them would also bite anyone building something similar:

| symptom | cause | fix |
|---|---|---|
| new servers never started sshd | my cloud-init boothook ran `systemctl enable --now` for a unit ordered after `network-online.target`, which waits for the very cloud-init stage the boothook runs in | `systemctl start --no-block` |
| writing to `/dev/nvme-fabrics` fails with `Invalid argument` | the kernel logs "found same hostid but different hostnqn": a custom host NQN needs its own host ID | derive a host ID from the server ID |
| any VM could connect to any volume | nvmet host ACLs trust whatever NQN the initiator sends | DH-HMAC-CHAP. Both Debian kernels have `NVME_HOST_AUTH` and `NVME_TARGET_AUTH`; each server gets a key derived from a master secret, delivered only on its own seed disk. Claiming another server's NQN now fails with `host response mismatch` |
| Kubernetes workers went to VM state `error` when I restarted the switch | a UDP socket connected to a closed port reports `ECONNREFUSED`, and Virtualization.framework stops the VM on any error on its network file handle | the helper gives the framework a unix socket pair and relays to the switch itself, dropping frames while the switch is away |
| CSI node plugins crashlooped after a node reboot | the CCM's route controller adds a network route per node's pod CIDR, and my driver installed the route to the node's *own* pod CIDR via its *own* private IP, shadowing the local `cni0` route. On Hetzner such routes live in the network gateway | skip routes whose gateway is one of the server's own addresses |
| 240–600 Mbit/s instead of the prototype's 1 Gbit/s | Go's network poller cost a goroutine wake-up per frame in the helper and in the switch, and the switch's eight reader goroutines reordered frames within TCP flows | blocking `recvfrom`/`sendto` on locked OS threads, and a single reader: 969 Mbit/s on a private network with MTU 1450 |

The reordering one surprised me most. More readers looked like free parallelism. But every out-of-order segment makes TCP think a packet was lost, and the retransmissions cost far more than the extra cores gained: 240 Mbit/s with eight readers against 969 Mbit/s with one. Per-flow sharding would bring the cores back, but one reader already saturates what a lab needs.

## The code

The files are next to this post in `poc/`:

| file | what |
|---|---|
| `vzprobe/main.go` | VM runner: EFI boot, NAT NIC, optional switch NIC and data disk, USB and NBD hot-plug over a TCP control port |
| `vzprobe/vz.entitlements` | the virtualization entitlement for the ad-hoc signature |
| `vzswitch/main.go` | the userspace switch with per-network learning and a control port |
| `make-vm.sh` | root disk clone and FAT NoCloud seed |
| `appliance.sh` | iSCSI and NVMe/TCP exports on the appliance VM |
| `bench.sh`, `table.py` | the fio jobs and the table above; raw results in `fio/` |

Typical run:

```sh
./vzswitch -port 17101=1 -port 17102=1 &
./vzprobe -dir vm1  -mac 52:54:00:0a:00:01 -ctl 127.0.0.1:17001 \
  -switch 127.0.0.1:17100 -switch-port 17101 -mac2 52:54:00:0b:00:01 -mtu2 9000 &
./vzprobe -dir stor -mac 52:54:00:0a:00:02 -ctl 127.0.0.1:17002 -cpus 4 -mem 4096 \
  -switch 127.0.0.1:17100 -switch-port 17102 -mac2 52:54:00:0b:00:02 -mtu2 9000 -disk stor/data.raw &
printf 'attach-usb /path/to/volume.raw\n' | nc 127.0.0.1 17001
printf 'set 17101 2\n' | nc 127.0.0.1 17199      # move vm1's switch port to network 2
```


### `vzprobe/main.go`

```go
// vzprobe runs one Linux VM with Virtualization.framework and accepts control
// commands on a localhost TCP port (spike, not product code):
//
//	attach-usb <disk> | attach-usb-nbd <nbd-url> | detach-usb <n> | list-usb | stop
package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"net/netip"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/Code-Hex/vz/v3"
)

func main() {
	dir := flag.String("dir", "", "VM directory (root.raw, seed.iso, efi, console.log, ctl.sock)")
	cpus := flag.Uint("cpus", 2, "")
	memMB := flag.Uint64("mem", 2048, "")
	mac := flag.String("mac", "", "MAC address")
	nested := flag.Bool("nested", false, "")
	ctl := flag.String("ctl", "127.0.0.1:17001", "control listen address")
	swAddr := flag.String("switch", "", "vzswitch UDP address for a second NIC, e.g. 127.0.0.1:17100")
	swPort := flag.Int("switch-port", 0, "local UDP port of the second NIC (identifies the switch port)")
	mac2 := flag.String("mac2", "", "MAC address of the second NIC")
	mtu2 := flag.Int("mtu2", 1500, "MTU of the second NIC")
	extra := flag.String("disk", "", "extra virtio disk (raw file), e.g. a data disk")
	flag.Parse()

	efi, err := vz.NewEFIVariableStore(filepath.Join(*dir, "efi"), vz.WithCreatingEFIVariableStore())
	if os.IsExist(err) || (err != nil && strings.Contains(err.Error(), "exist")) {
		efi, err = vz.NewEFIVariableStore(filepath.Join(*dir, "efi"))
	}
	must(err)
	boot, err := vz.NewEFIBootLoader(vz.WithEFIVariableStore(efi))
	must(err)
	cfg, err := vz.NewVirtualMachineConfiguration(boot, *cpus, *memMB<<20)
	must(err)

	platform, err := vz.NewGenericPlatformConfiguration()
	must(err)
	if *nested {
		must(platform.SetNestedVirtualizationEnabled(true))
	}
	cfg.SetPlatformVirtualMachineConfiguration(platform)

	var disks []vz.StorageDeviceConfiguration
	for _, d := range []struct {
		file string
		ro   bool
	}{{"root.raw", false}, {"seed.iso", true}} {
		att, err := vz.NewDiskImageStorageDeviceAttachment(filepath.Join(*dir, d.file), d.ro)
		must(err)
		blk, err := vz.NewVirtioBlockDeviceConfiguration(att)
		must(err)
		disks = append(disks, blk)
	}
	if *extra != "" {
		att, err := vz.NewDiskImageStorageDeviceAttachment(*extra, false)
		must(err)
		blk, err := vz.NewVirtioBlockDeviceConfiguration(att)
		must(err)
		disks = append(disks, blk)
	}
	cfg.SetStorageDevicesVirtualMachineConfiguration(disks)

	nat, err := vz.NewNATNetworkDeviceAttachment()
	must(err)
	nic, err := vz.NewVirtioNetworkDeviceConfiguration(nat)
	must(err)
	if *mac != "" {
		hw, err := net.ParseMAC(*mac)
		must(err)
		m, err := vz.NewMACAddress(hw)
		must(err)
		nic.SetMACAddress(m)
	}
	nics := []*vz.VirtioNetworkDeviceConfiguration{nic}
	if *swAddr != "" {
		f, err := switchSocket(*swPort, *swAddr)
		must(err)
		fh, err := vz.NewFileHandleNetworkDeviceAttachment(f)
		must(err)
		if *mtu2 != 1500 {
			must(fh.SetMaximumTransmissionUnit(*mtu2))
		}
		nic2, err := vz.NewVirtioNetworkDeviceConfiguration(fh)
		must(err)
		hw, err := net.ParseMAC(*mac2)
		must(err)
		m, err := vz.NewMACAddress(hw)
		must(err)
		nic2.SetMACAddress(m)
		nics = append(nics, nic2)
	}
	cfg.SetNetworkDevicesVirtualMachineConfiguration(nics)

	serialAtt, err := vz.NewFileSerialPortAttachment(filepath.Join(*dir, "console.log"), false)
	must(err)
	serial, err := vz.NewVirtioConsoleDeviceSerialPortConfiguration(serialAtt)
	must(err)
	cfg.SetSerialPortsVirtualMachineConfiguration([]*vz.VirtioConsoleDeviceSerialPortConfiguration{serial})

	entropy, err := vz.NewVirtioEntropyDeviceConfiguration()
	must(err)
	cfg.SetEntropyDevicesVirtualMachineConfiguration([]*vz.VirtioEntropyDeviceConfiguration{entropy})

	xhci, err := vz.NewXHCIControllerConfiguration()
	must(err)
	cfg.SetUSBControllersVirtualMachineConfiguration([]vz.USBControllerConfiguration{xhci})

	ok, err := cfg.Validate()
	if !ok || err != nil {
		log.Fatalf("invalid config: %v", err)
	}
	vm, err := vz.NewVirtualMachine(cfg)
	must(err)
	must(vm.Start())
	log.Printf("started, state %v", vm.State())

	var mu sync.Mutex
	usb := map[int]vz.USBDevice{}
	next := 0

	l, err := net.Listen("tcp", *ctl)
	must(err)
	go func() {
		for st := range vm.StateChangedNotify() {
			log.Printf("state %v", st)
			if st == vz.VirtualMachineStateStopped || st == vz.VirtualMachineStateError {
				os.Exit(0)
			}
		}
	}()
	for {
		c, err := l.Accept()
		if err != nil {
			continue
		}
		go func(c net.Conn) {
			defer c.Close()
			line, _ := bufio.NewReader(c).ReadString('\n')
			f := strings.Fields(line)
			if len(f) == 0 {
				return
			}
			reply := func(format string, a ...any) { fmt.Fprintf(c, format+"\n", a...) }
			start := time.Now()
			switch f[0] {
			case "attach-usb", "attach-usb-nbd":
				var att vz.StorageDeviceAttachment
				if f[0] == "attach-usb" {
					att, err = vz.NewDiskImageStorageDeviceAttachment(f[1], false)
				} else {
					var nbd *vz.NetworkBlockDeviceStorageDeviceAttachment
					nbd, err = vz.NewNetworkBlockDeviceStorageDeviceAttachment(f[1], 10*time.Second, false, vz.DiskSynchronizationModeFull)
					att = nbd
				}
				if err != nil {
					reply("error: %v", err)
					return
				}
				dc, err := vz.NewUSBMassStorageDeviceConfiguration(att)
				if err != nil {
					reply("error: %v", err)
					return
				}
				dev, err := vz.NewUSBMassStorageDevice(dc)
				if err != nil {
					reply("error: %v", err)
					return
				}
				if err := vm.USBControllers()[0].Attach(dev); err != nil {
					reply("error: %v", err)
					return
				}
				mu.Lock()
				next++
				usb[next] = dev
				mu.Unlock()
				reply("attached %d in %v", next, time.Since(start))
			case "detach-usb":
				n, _ := strconv.Atoi(f[1])
				mu.Lock()
				dev := usb[n]
				delete(usb, n)
				mu.Unlock()
				if dev == nil {
					reply("error: no device %d", n)
					return
				}
				if err := vm.USBControllers()[0].Detach(dev); err != nil {
					reply("error: %v", err)
					return
				}
				reply("detached %d in %v", n, time.Since(start))
			case "list-usb":
				mu.Lock()
				reply("%d devices: %v", len(usb), usb)
				mu.Unlock()
			case "stop":
				ok, err := vm.RequestStop()
				reply("request stop: %v %v", ok, err)
			default:
				reply("unknown command")
			}
		}(c)
	}
}

// switchSocket returns a UDP socket bound to 127.0.0.1:localPort and connected
// to the switch, with the buffer sizes the framework asks for.
func switchSocket(localPort int, switchAddr string) (*os.File, error) {
	ap, err := netip.ParseAddrPort(switchAddr)
	if err != nil {
		return nil, err
	}
	fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_DGRAM, 0)
	if err != nil {
		return nil, err
	}
	for opt, v := range map[int]int{syscall.SO_SNDBUF: 2 << 20, syscall.SO_RCVBUF: 8 << 20} {
		if err := syscall.SetsockoptInt(fd, syscall.SOL_SOCKET, opt, v); err != nil {
			return nil, err
		}
	}
	if err := syscall.Bind(fd, &syscall.SockaddrInet4{Port: localPort, Addr: [4]byte{127, 0, 0, 1}}); err != nil {
		return nil, fmt.Errorf("bind: %w", err)
	}
	if err := syscall.Connect(fd, &syscall.SockaddrInet4{Port: int(ap.Port()), Addr: ap.Addr().As4()}); err != nil {
		return nil, fmt.Errorf("connect: %w", err)
	}
	return os.NewFile(uintptr(fd), "switch"), nil
}

func must(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
```

### `vzswitch/main.go`

```go
// vzswitch is a prototype userspace Ethernet switch for Virtualization.framework
// VMs. Each VM NIC is a UDP socket bound to a fixed local port and connected to
// the switch; one datagram carries one Ethernet frame. The switch assigns a port
// (the VM's UDP source port, not something the guest controls) to a network and
// only forwards frames between ports of the same network: learning by source
// MAC per network, flooding broadcast and unknown unicast.
//
// Control (TCP, one command per connection):
//
//	set <udp-port> <network>   assign or move a port (0 detaches it)
//	stats                      ports, networks, MAC tables, counters
package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"net/netip"
	"sort"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"syscall"
)

type port struct {
	addr    netip.AddrPort
	network int
	rx, tx  atomic.Uint64
}

type sw struct {
	conn *net.UDPConn

	mu    sync.RWMutex
	ports map[uint16]*port                   // by UDP source port
	fdb   map[int]map[[6]byte]netip.AddrPort // network -> MAC -> port address
	drops atomic.Uint64
}

func main() {
	listen := flag.String("listen", "127.0.0.1:17100", "switch UDP address")
	ctl := flag.String("ctl", "127.0.0.1:17199", "control TCP address")
	var assign multiFlag
	flag.Var(&assign, "port", "udp-port=network, repeatable")
	flag.Parse()

	addr, err := net.ResolveUDPAddr("udp", *listen)
	must(err)
	conn, err := net.ListenUDP("udp", addr)
	must(err)
	must(setBuffers(conn))
	s := &sw{conn: conn, ports: map[uint16]*port{}, fdb: map[int]map[[6]byte]netip.AddrPort{}}
	for _, a := range assign {
		p, n, _ := strings.Cut(a, "=")
		pn, _ := strconv.Atoi(p)
		nn, _ := strconv.Atoi(n)
		s.set(uint16(pn), nn)
	}
	go s.control(*ctl)
	log.Printf("switch on %s, control on %s", *listen, *ctl)

	buf := make([]byte, 65536)
	for {
		n, from, err := conn.ReadFromUDPAddrPort(buf)
		if err != nil {
			log.Printf("read: %v", err)
			continue
		}
		s.forward(buf[:n], from)
	}
}

func (s *sw) forward(frame []byte, from netip.AddrPort) {
	if len(frame) < 14 {
		return
	}
	s.mu.RLock()
	src := s.ports[from.Port()]
	s.mu.RUnlock()
	if src == nil || src.network == 0 || src.addr != from {
		s.drops.Add(1)
		return
	}
	src.rx.Add(1)
	var dst, smac [6]byte
	copy(dst[:], frame[0:6])
	copy(smac[:], frame[6:12])

	s.mu.Lock()
	table := s.fdb[src.network]
	if table == nil {
		table = map[[6]byte]netip.AddrPort{}
		s.fdb[src.network] = table
	}
	table[smac] = from
	target, known := table[dst]
	var flood []netip.AddrPort
	if !known || dst[0]&1 == 1 {
		for _, p := range s.ports {
			if p.network == src.network && p.addr != from {
				flood = append(flood, p.addr)
			}
		}
	}
	s.mu.Unlock()

	send := func(to netip.AddrPort) {
		if _, err := s.conn.WriteToUDPAddrPort(frame, to); err != nil {
			s.drops.Add(1)
			return
		}
		s.mu.RLock()
		if p := s.ports[to.Port()]; p != nil {
			p.tx.Add(1)
		}
		s.mu.RUnlock()
	}
	if known && dst[0]&1 == 0 {
		send(target)
		return
	}
	for _, to := range flood {
		send(to)
	}
}

// set assigns a UDP port to a network; moving a port forgets its MACs.
func (s *sw) set(udpPort uint16, network int) {
	s.mu.Lock()
	defer s.mu.Unlock()
	addr := netip.AddrPortFrom(netip.MustParseAddr("127.0.0.1"), udpPort)
	for _, table := range s.fdb {
		for mac, a := range table {
			if a == addr {
				delete(table, mac)
			}
		}
	}
	if network == 0 {
		delete(s.ports, udpPort)
		return
	}
	if p := s.ports[udpPort]; p != nil {
		p.network = network
		return
	}
	s.ports[udpPort] = &port{addr: addr, network: network}
}

func (s *sw) control(addr string) {
	l, err := net.Listen("tcp", addr)
	must(err)
	for {
		c, err := l.Accept()
		if err != nil {
			continue
		}
		line, _ := bufio.NewReader(c).ReadString('\n')
		f := strings.Fields(line)
		switch {
		case len(f) == 3 && f[0] == "set":
			p, _ := strconv.Atoi(f[1])
			n, _ := strconv.Atoi(f[2])
			s.set(uint16(p), n)
			fmt.Fprintf(c, "port %d -> network %d\n", p, n)
		case len(f) == 1 && f[0] == "stats":
			s.mu.RLock()
			var keys []int
			for k := range s.ports {
				keys = append(keys, int(k))
			}
			sort.Ints(keys)
			for _, k := range keys {
				p := s.ports[uint16(k)]
				fmt.Fprintf(c, "port %d network %d rx %d tx %d\n", k, p.network, p.rx.Load(), p.tx.Load())
			}
			for n, t := range s.fdb {
				for mac, a := range t {
					fmt.Fprintf(c, "fdb network %d %x -> %d\n", n, mac, a.Port())
				}
			}
			fmt.Fprintf(c, "drops %d\n", s.drops.Load())
			s.mu.RUnlock()
		default:
			fmt.Fprintln(c, "usage: set <udp-port> <network> | stats")
		}
		c.Close()
	}
}

func setBuffers(c *net.UDPConn) error {
	raw, err := c.SyscallConn()
	if err != nil {
		return err
	}
	var serr error
	err = raw.Control(func(fd uintptr) {
		if serr = syscall.SetsockoptInt(int(fd), syscall.SOL_SOCKET, syscall.SO_SNDBUF, 4<<20); serr != nil {
			return
		}
		serr = syscall.SetsockoptInt(int(fd), syscall.SOL_SOCKET, syscall.SO_RCVBUF, 8<<20)
	})
	if err != nil {
		return err
	}
	return serr
}

type multiFlag []string

func (m *multiFlag) String() string     { return strings.Join(*m, ",") }
func (m *multiFlag) Set(v string) error { *m = append(*m, v); return nil }

func must(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
```

### `make-vm.sh`

```sh
#!/bin/sh
# make-vm.sh <dir> <name> <nat-mac> <ssh-public-key-file>: root disk clone and NoCloud seed for vzprobe.
# The seed is a FAT disk labeled CIDATA: an ISO 9660 seed on a virtio disk was ignored by cloud-init.
set -eu
dir=$1 name=$2 mac=$3 key=$4
mkdir -p "$dir/seed"
/bin/cp -c debian-13-generic-arm64.raw "$dir/root.raw"   # APFS clone, instant
truncate -s 20G "$dir/root.raw"
cat > "$dir/seed/meta-data" <<EOT
instance-id: $name
local-hostname: $name
public-keys:
  - $(cat "$key")
EOT
printf '#cloud-config\ndisable_root: false\n' > "$dir/seed/user-data"
cat > "$dir/seed/network-config" <<EOT
version: 2
ethernets:
  eth0:
    match: {macaddress: "$mac"}
    set-name: eth0
    dhcp4: true
    dhcp-identifier: mac   # otherwise the macOS DHCP server keys the lease by DUID
EOT
hdiutil create -quiet -fs "MS-DOS FAT12" -volname CIDATA -srcfolder "$dir/seed" -format UDRW -size 4m "$dir/seed.dmg"
dev=$(hdiutil attach -nomount "$dir/seed.dmg" | head -1 | awk '{print $1}')
/bin/dd if="$(echo "$dev" | sed s/disk/rdisk/)" of="$dir/seed.iso" bs=1m 2>/dev/null
hdiutil detach "$dev" >/dev/null
```

### `appliance.sh`

```sh
#!/bin/sh
# Storage appliance (Debian 13 VM, data disk /dev/vdc, switch NIC 10.99.0.2/24 with MTU 9000).
# Exports one LV over iSCSI (LIO) and one over NVMe/TCP (nvmet). Spike only: no authentication.
set -eu
CLIENT_IQN=${1:?client initiator name, from /etc/iscsi/initiatorname.iscsi}
apt-get install -y targetcli-fb lvm2
modprobe nvmet nvmet-tcp
pvcreate /dev/vdc && vgcreate vols /dev/vdc
lvcreate -L 20G -n iscsi vols && lvcreate -L 18G -n nvme vols

# iSCSI: the backstore name becomes the SCSI model, the serial must be set before export
T=iqn.2026-09.io.ownpaas:srv-1
targetcli /backstores/block create HC_Volume_301 /dev/vols/iscsi
echo HC_Volume_301 > /sys/kernel/config/target/core/iblock_0/HC_Volume_301/wwn/vpd_unit_serial
targetcli /backstores/block/HC_Volume_301 set attribute emulate_model_alias=1
targetcli /iscsi create $T
targetcli /iscsi/$T/tpg1 set attribute authentication=0
targetcli /iscsi/$T/tpg1/luns create /backstores/block/HC_Volume_301 add_mapped_luns=false
targetcli /iscsi/$T/tpg1/acls create "$CLIENT_IQN"

# NVMe/TCP: plain configfs, model and serial are free-form
N=/sys/kernel/config/nvmet
S=$N/subsystems/hc-volume-302
mkdir -p $S/namespaces/1
echo 1 > $S/attr_allow_any_host
echo HC_Volume_302 > $S/attr_serial
echo HC_Volume_302 > $S/attr_model
echo /dev/vols/nvme > $S/namespaces/1/device_path
echo 1 > $S/namespaces/1/enable
mkdir -p $N/ports/1
echo 10.99.0.2 > $N/ports/1/addr_traddr
echo tcp > $N/ports/1/addr_trtype
echo 4420 > $N/ports/1/addr_trsvcid
echo ipv4 > $N/ports/1/addr_adrfam
ln -s $S $N/ports/1/subsystems/

# client side:
#   iscsiadm -m discovery -t st -p 10.99.0.2 && iscsiadm -m node -T $T -p 10.99.0.2:3260 --login
#   nvme connect -t tcp -a 10.99.0.2 -s 4420 -n hc-volume-302
#   (without nvme-cli: echo "transport=tcp,traddr=10.99.0.2,trsvcid=4420,nqn=hc-volume-302" > /dev/nvme-fabrics)
```

### `bench.sh`

```sh
#!/bin/sh
# bench.sh <name> <device>: raw-device fio jobs, then an etcd-style fdatasync test on ext4
set -eu
name=$1 dev=$2 out=/root/bench/$1; mkdir -p $out
run() { fio --name=$1 --filename=$dev --direct=1 --ioengine=libaio --time_based --runtime=${RT:-20} --group_reporting --output-format=json --output=$out/$1.json "$@" >/dev/null 2>&1 || true; }
job() { n=$1; shift; fio --name=$n --filename=$dev --direct=1 --ioengine=libaio --time_based --runtime=20 --group_reporting --output-format=json --output=$out/$n.json "$@" >/dev/null; }
job randread  --rw=randread  --bs=4k --iodepth=32 --numjobs=1
job randwrite --rw=randwrite --bs=4k --iodepth=32 --numjobs=1
job randrw    --rw=randrw --rwmixread=70 --bs=4k --iodepth=16 --numjobs=2
job lat-qd1   --rw=randwrite --bs=4k --iodepth=1 --numjobs=1
job seqwrite  --rw=write --bs=1M --iodepth=4 --numjobs=1
job seqread   --rw=read  --bs=1M --iodepth=4 --numjobs=1
mkfs.ext4 -q -F $dev; mkdir -p /mnt/bench; mount $dev /mnt/bench
fio --name=etcd --directory=/mnt/bench --rw=write --ioengine=sync --fdatasync=1 --size=22m --bs=2300 --output-format=json --output=$out/etcd.json >/dev/null
umount /mnt/bench
echo done $name
```

### `table.py`

```python
import json,sys
base=sys.argv[1]
names=['virtio','usb','iscsi','nvmetcp']
def load(n,j): return json.load(open(f'{base}/{n}/{j}.json'))['jobs'][0]
print("| metric | "+" | ".join(names)+" |"); print("|---"*(len(names)+1)+"|")
def row(label,f):
    vals=[]
    for n in names:
        try: vals.append(f(n))
        except Exception as e: vals.append('err')
    print(f"| {label} | "+" | ".join(vals)+" |")
row("4k randread qd32 IOPS", lambda n: f"{load(n,'randread')['read']['iops']:,.0f}")
row("4k randwrite qd32 IOPS", lambda n: f"{load(n,'randwrite')['write']['iops']:,.0f}")
row("4k randrw 70/30 qd16x2 IOPS", lambda n: f"{load(n,'randrw')['read']['iops']+load(n,'randrw')['write']['iops']:,.0f}")
row("4k randwrite qd1 IOPS", lambda n: f"{load(n,'lat-qd1')['write']['iops']:,.0f}")
row("4k randwrite qd1 p99 (ms)", lambda n: f"{load(n,'lat-qd1')['write']['clat_ns']['percentile']['99.000000']/1e6:.2f}")
row("1M seq write MB/s", lambda n: f"{load(n,'seqwrite')['write']['bw_bytes']/1e6:,.0f}")
row("1M seq read MB/s", lambda n: f"{load(n,'seqread')['read']['bw_bytes']/1e6:,.0f}")
def etcd(n,p): return f"{load(n,'etcd')['sync']['lat_ns']['percentile'][p]/1e6:.2f}"
row("etcd fdatasync p50 (ms)", lambda n: etcd(n,'50.000000'))
row("etcd fdatasync p99 (ms)", lambda n: etcd(n,'99.000000'))
row("etcd write IOPS", lambda n: f"{load(n,'etcd')['write']['iops']:,.0f}")
```

