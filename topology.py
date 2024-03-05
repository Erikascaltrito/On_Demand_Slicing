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
        # aggiungo
        
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
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        # creo topologia a stella con controller in mezzo
        self.addLink("s6","s2")
        self.addLink("s6","s3")
        self.addLink("s6","s4")
        self.addLink("s6","s5")
        
        # collego pc agli switch per office1
        self.addLink("s2","h1")
        self.addLink("s2","h3")
        self.addLink("s3","h4")
        self.addLink("s3","h5")
        
        # collego pc agli switch per office2
        self.addLink("s4","h2")
        self.addLink("s4","h6")
        self.addLink("s5","h7")
        self.addLink("s5","h8")
        
        # collego pc allo switch per office3
        self.addLink("s1","h9")
        self.addLink("s1","h10")
        
        
        self.addLink("s1","r1",intfName2='r2-eth1',params2={'ip':'192.168.3.1/24'})
        self.addLink("s6","r2",intfName2='r2-eth1',params2={'ip':'192.168.3.1/24'})
        
        self.addLink(r1,
                     r2,
                     intfName1='r1-eth2',
                     intfName2='r2-eth2',
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
    controller = RemoteController("c0", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.start()

    # setup router
    net['r1'].cmd("sudo ip route add 192.168.3.0/24 via 10.100.0.2 dev r1-eth2")
    net['r2'].cmd("sudo ip route add 192.168.2.0/24 via 10.100.0.1 dev r2-eth2")

    
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    runTopo()