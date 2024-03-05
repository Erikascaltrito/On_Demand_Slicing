import os
import shutil
import sys
import time
import math

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSKernelSwitch, RemoteController, Node
from mininet.link import TCLink

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class Topology(Topo):

    def build(self):
        
        # aggiungo gli host
        h1 = self.addHost("h1", ip="192.168.2.21/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:01')
        h2 = self.addHost("h2", ip="192.168.2.41/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:02')
        
        h3 = self.addHost("h3", ip="192.168.2.22/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:03')
        h4 = self.addHost("h4", ip="192.168.2.31/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:04')
        h5 = self.addHost("h5", ip="192.168.2.32/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:05')
        h6 = self.addHost("h6", ip="192.168.2.42/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:06')
        h7 = self.addHost("h7", ip="192.168.2.51/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:07')
        h8 = self.addHost("h8", ip="192.168.2.52/24",defaultRoute='via 192.168.2.1',mac='00:00:00:00:00:08')

        h9 = self.addHost("h9", ip="192.168.3.61/24",defaultRoute='via 192.168.3.1',mac='00:00:00:00:00:09')
        h10 = self.addHost("h10", ip="192.168.3.62/24",defaultRoute='via 192.168.3.1',mac='00:00:00:00:00:0a')

        # aggiungo i router
        r1 = self.addHost("r1",cls=LinuxRouter,ip="192.168.2.1/24",mac='00:00:00:00:00:0e')
        r2 = self.addHost("r2",cls=LinuxRouter,ip="192.168.3.1/24",mac='00:00:00:00:00:0f')
        
        # aggiungo gli switch
        for i in range(6):
            #sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), cls=OVSKernelSwitch)

        # Collego gli switch tra loro
        self.addLink("s6", "s2", intfName1='s6-eth1', intfName2='s2-eth1')
        self.addLink("s6", "s3", intfName1='s6-eth2', intfName2='s3-eth1')
        self.addLink("s6", "s4", intfName1='s6-eth3', intfName2='s4-eth1')
        self.addLink("s6", "s5", intfName1='s6-eth4', intfName2='s5-eth1')

        # Collego gli switch agli host
        self.addLink("s2", "h1", intfName1='s2-eth2', intfName2='h1-eth0')
        self.addLink("s2", "h3", intfName1='s2-eth3', intfName2='h3-eth0')
        self.addLink("s3", "h4", intfName1='s3-eth2', intfName2='h4-eth0')
        self.addLink("s3", "h5", intfName1='s3-eth3', intfName2='h5-eth0')

        self.addLink("s4", "h2", intfName1='s4-eth2', intfName2='h2-eth0')
        self.addLink("s4", "h6", intfName1='s4-eth3', intfName2='h6-eth0')
        self.addLink("s5", "h7", intfName1='s5-eth2', intfName2='h7-eth0')
        self.addLink("s5", "h8", intfName1='s5-eth3', intfName2='h8-eth0')

        self.addLink("s1", "h9", intfName1='s1-eth2', intfName2='h9-eth0')
        self.addLink("s1", "h10", intfName1='s1-eth3', intfName2='h10-eth0')

        # Collego gli switch ai router
        self.addLink("s1", "r1", intfName1='s1-eth1', intfName2='r1-eth1')
        self.addLink("s6", "r2", intfName1='s6-eth5', intfName2='r2-eth1')

        # Collego i router tra loro
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})

def runTopo():
    topo = Topology()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    c0 = net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.addController(c0)


    net.build()
    
    net['r1'].cmd("sudo ip route add 192.168.3.0/24 via 10.100.0.2 dev r1-eth2")
    net['r2'].cmd("sudo ip route add 192.168.2.0/24 via 10.100.0.1 dev r2-eth2")

    for controller in net.controllers:
        controller.start()
   
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    
    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    runTopo()