from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from _thread import start_new_thread
import os, stat
import json
import time
import csv
import requests
import sys
from config import Config

sys.path.append("./controller")
sys.path.append(".")
print(os.getcwd())
print(sys.path.__str__())

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


def startIperf(host1, host2, bw, port, timeTotal):
    # host2.cmd("iperf -s -u -p {} &".format(port))
    print("Host {} to Host {} Bandwidth: {}".format(host1.name, host2.name, bw))
    command = "iperf -c {} -u -p {} -t {} -b {}M &".format(host2.IP(), port, timeTotal, bw)
    host1.cmd(command)

def min_to_sec(min):
    return min * 60


def runTopo():
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8', link=TCLink)

    queue_lenght = Config.queue_lenght
    timeTotal = min_to_sec(Config.duration_iperf_per_load_level_minutes)
    controllerIP = '127.0.0.1'
    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip=controllerIP,
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)

    r1 = net.addHost("r1",cls=LinuxRouter,ip="192.168.2.1/24",mac='00:00:00:00:00:0e')
    r2 = net.addHost("r2",cls=LinuxRouter,ip="192.168.3.1/24",mac='00:00:00:00:00:0f')

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip="192.168.2.21/24", defaultRoute=None, mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', cls=Host, ip="192.168.2.22/24", defaultRoute=None, mac='00:00:00:00:00:02')

    h3 = net.addHost('h3', cls=Host, ip="192.168.2.31/24", defaultRoute=None, mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', cls=Host, ip="192.168.2.32/24", defaultRoute=None, mac='00:00:00:00:00:04')

    h5 = net.addHost('h5', cls=Host, ip="192.168.2.41/24", defaultRoute=None, mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', cls=Host, ip="192.168.2.42/24", defaultRoute=None, mac='00:00:00:00:00:06')

    h7 = net.addHost('h7', cls=Host, ip="192.168.2.51/24", defaultRoute=None, mac='00:00:00:00:00:07')
    h8 = net.addHost('h8', cls=Host, ip="192.168.2.52/24", defaultRoute=None, mac='00:00:00:00:00:08')

    h9 = net.addHost('h9', cls=Host, ip="192.168.2.61/24", defaultRoute=None, mac='00:00:00:00:00:09')
    h10 = net.addHost('h10', cls=Host, ip="192.168.2.62/24", defaultRoute=None, mac='00:00:00:00:00:0a')

    info('*** Add links\n')
     # Collego gli switch tra loro
    net.addLink("s6", "s2", intfName1='s6-eth1', intfName2='s2-eth1')
    net.addLink("s6", "s3", intfName1='s6-eth2', intfName2='s3-eth1')
    net.addLink("s6", "s4", intfName1='s6-eth3', intfName2='s4-eth1')
    net.addLink("s6", "s5", intfName1='s6-eth4', intfName2='s5-eth1')

    # Collego gli switch agli host
    net.addLink("s2", "h1", intfName1='s2-eth2', intfName2='h1-eth0')
    net.addLink("s2", "h2", intfName1='s2-eth3', intfName2='h3-eth0')

    net.addLink("s3", "h3", intfName1='s3-eth2', intfName2='h4-eth0')
    net.addLink("s3", "h4", intfName1='s3-eth3', intfName2='h5-eth0')

    net.addLink("s4", "h5", intfName1='s4-eth2', intfName2='h2-eth0')
    net.addLink("s4", "h6", intfName1='s4-eth3', intfName2='h6-eth0')

    net.addLink("s5", "h7", intfName1='s5-eth2', intfName2='h7-eth0')
    net.addLink("s5", "h8", intfName1='s5-eth3', intfName2='h8-eth0')

    net.addLink("s1", "h9", intfName1='s1-eth2', intfName2='h9-eth0')
    net.addLink("s1", "h10", intfName1='s1-eth3', intfName2='h10-eth0')

    # Collego gli switch ai router
    net.addLink("s1", "r1", intfName1='s1-eth1', intfName2='r1-eth1')
    net.addLink("s6", "r2", intfName1='s6-eth5', intfName2='r2-eth1')

    # Collego i router tra loro
    net.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
    
    #('*** Starting network\n')
    net.build()

    net['r1'].cmd("sudo ip route add 192.168.3.0/24 via 10.100.0.2 dev r1-eth2")
    net['r2'].cmd("sudo ip route add 192.168.2.0/24 via 10.100.0.1 dev r2-eth2")

    #('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    #('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])

    time.sleep(15)

    #print("Starting iperf ")  #ricordarsi di aggiungere gli host
    #start_new_thread(startIperf, (h1, h4, 2.75, 5001, timeTotal))
    #start_new_thread(startIperf, (h2, h5, 1.75, 5001, timeTotal))
    #start_new_thread(startIperf, (h3, h6, 1.75, 5001, timeTotal))
    #time.sleep(timeTotal)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

runTopo()
