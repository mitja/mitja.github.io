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
