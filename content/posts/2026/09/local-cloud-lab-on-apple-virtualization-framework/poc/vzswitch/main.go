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
