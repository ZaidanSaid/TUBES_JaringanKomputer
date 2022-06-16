#Zaidan Said
#1301200331

from mininet.net import Mininet
from mininet.link import TCLink, Link, Intf
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from subprocess import Popen, PIPE
from time import sleep
import os


if '__main__' == __name__:
	os.system("mn -c")
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.enabled"
	value = 1
	p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=", stdout, "stderr=", stderr)
	
    #CLO1
	#Host dan Router
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')
	
	#Link antara host dan router
	net.addLink(r1, h1, intfName1 = 'r1-eth0', intfName2 = 'h1-eth0', cls=TCLink, max_queue_size = 100, use_tbf = True, bw=1)
	net.addLink(r1, r3, intfName1 = 'r1-eth1', intfName2 = 'r3-eth1', cls=TCLink, max_queue_size = 100, use_tbf = True, bw=0.5)
	net.addLink(r1, r4, intfName1 = 'r1-eth2', intfName2 = 'r4-eth2', cls=TCLink, max_queue_size = 100, use_tbf = True, bw=1)
			
	net.addLink(r2, h1, intfName1 = 'r2-eth1', intfName2 = 'h1-eth1', cls=TCLink, max_queue_size = 100, use_tbf=True, bw=1)	
	net.addLink(r2, r4, intfName1 = 'r2-eth0', intfName2 = 'r4-eth0', cls=TCLink, max_queue_size = 100, use_tbf=True, bw=0.5)
	net.addLink(r2, r3, intfName1 = 'r2-eth2', intfName2 = 'r3-eth2', cls=TCLink, max_queue_size = 100, use_tbf=True, bw=1)
		
	net.addLink(r3, h2, intfName1 = 'r3-eth0', intfName2 = 'h2-eth0', cls=TCLink, max_queue_size = 100, use_tbf=True, bw=1)
	
	net.addLink(r4, h2, intfName1 = 'r4-eth1', intfName2 = 'h2-eth1', cls=TCLink, max_queue_size = 100, use_tbf=True, bw=1)
				
	net.build()
	
	#Config
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eth1 0")
	
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	
	h1.cmd("ifconfig h1-eth0 180.252.0.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 180.252.7.1 netmask 255.255.255.0")

	h2.cmd("ifconfig h2-eth0 180.252.4.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 180.252.5.2 netmask 255.255.255.0")
	
	r1.cmd("ifconfig r1-eth0 180.252.0.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 180.252.2.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 180.252.1.1 netmask 255.255.255.0")
	
	r2.cmd("ifconfig r2-eth0 180.252.6.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 180.252.7.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 180.252.3.1 netmask 255.255.255.0")
	
	r3.cmd("ifconfig r3-eth0 180.252.4.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 180.252.2.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 180.252.3.2 netmask 255.255.255.0")

	r4.cmd("ifconfig r4-eth0 180.252.6.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 180.252.5.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 180.252.1.2 netmask 255.255.255.0")
	
    #CLO2
	# IP 
	h1.cmd("ip rule add from 180.252.0.1 table 1")
	h1.cmd("ip rule add from 180.252.7.1 table 2")
	h1.cmd("ip route add 180.252.0.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 180.252.0.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 180.252.7.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 180.252.7.2 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 180.252.0.2 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 180.252.7.2 dev h1-eth1")
	
	h2.cmd("ip rule add from 180.252.4.2 table 1")
	h2.cmd("ip rule add from 180.252.5.2 table 2")
	h2.cmd("ip route add 180.252.4.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 180.252.4.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 180.252.5.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 180.252.5.1 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 180.252.4.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 180.252.5.1 dev h2-eth1")
	
	r1.cmd("route add -net 180.252.3.0/24 gw 180.252.2.2")
	r1.cmd("route add -net 180.252.4.0/24 gw 180.252.2.2")
	r1.cmd("route add -net 180.252.5.0/24 gw 180.252.1.2")
	r1.cmd("route add -net 180.252.6.0/24 gw 180.252.1.2")
	r1.cmd("route add -net 180.252.7.0/24 gw 180.252.2.2")
	
	r2.cmd("route add -net 180.252.0.0/24 gw 180.252.6.2")
	r2.cmd("route add -net 180.252.1.0/24 gw 180.252.6.2")
	r2.cmd("route add -net 180.252.2.0/24 gw 180.252.3.2")
	r2.cmd("route add -net 180.252.4.0/24 gw 180.252.3.2")
	r2.cmd("route add -net 180.252.5.0/24 gw 180.252.6.2")
	
	r3.cmd("route add -net 180.252.0.0/24 gw 180.252.2.1")
	r3.cmd("route add -net 180.252.1.0/24 gw 180.252.2.1")
	r3.cmd("route add -net 180.252.5.0/24 gw 180.252.3.1")
	r3.cmd("route add -net 180.252.6.0/24 gw 180.252.3.1")
	r3.cmd("route add -net 180.252.7.0/24 gw 180.252.3.1")
	
	r4.cmd("route add -net 180.252.0.0/24 gw 180.252.1.1")
	r4.cmd("route add -net 180.252.2.0/24 gw 180.252.1.1")
	r4.cmd("route add -net 180.252.3.0/24 gw 180.252.6.1")
	r4.cmd("route add -net 180.252.4.0/24 gw 180.252.6.1")
	r4.cmd("route add -net 180.252.7.0/24 gw 180.252.6.1")
	
	#CLO3
	h2.cmd("iperf -s &")
	
	#pcap
	h2.cmd("tcpdump -w tcp_1301200331.pcap &") # Capture Traffic using TCPDump
	
	h1.cmd("iperf -c 180.252.4.2 -t 100 &")
	sleep(10)
	h1.cmd("iperf -c 180.252.4.2")
	
	CLI(net)
	
	net.stop()
	
	
	
	
	
