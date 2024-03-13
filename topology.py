from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from _thread import start_new_thread
import time

def runTopo():
    net = Mininet(topo=None,
                  build=False,
                  #autoSetMacs=True,
                  #autoStaticArp=True,
                  ipBase='10.0.0.0/8', 
                  link=TCLink)
    
    controllerIP = '127.0.0.1'
    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip=controllerIP,
                           protocol='tcp',
                           port=6633)
    
    host_config = dict(inNamespace=True)
    http_link_config = dict(bw=1)
    video_conf_link_config = dict(bw=10)
    host_link_config = dict()
    
    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip="192.168.2.21/24", defaultRoute=None, mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', cls=Host, ip="192.168.2.22/24", defaultRoute=None, mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', cls=Host, ip="192.168.2.23/24", defaultRoute=None, mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', cls=Host, ip="192.168.2.24/24", defaultRoute=None, mac='00:00:00:00:00:04')

    h5 = net.addHost('h5', cls=Host, ip="192.168.2.41/24", defaultRoute=None, mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', cls=Host, ip="192.168.2.42/24", defaultRoute=None, mac='00:00:00:00:00:06')
    h7 = net.addHost('h7', cls=Host, ip="192.168.2.43/24", defaultRoute=None, mac='00:00:00:00:00:07')
    h8 = net.addHost('h8', cls=Host, ip="192.168.2.44/24", defaultRoute=None, mac='00:00:00:00:00:08')

    h9  =net.addHost('h9', cls=Host, ip="192.168.2.51/24", defaultRoute=None, mac='00:00:00:00:00:09')
    h10 = net.addHost('h10', cls=Host, ip="192.168.2.52/24", defaultRoute=None, mac='00:00:00:00:00:0a')

    h11 = net.addHost('h11', cls=Host, ip="192.168.2.61/24", defaultRoute=None, mac='00:00:00:00:00:0b')
    h12 = net.addHost('h12', cls=Host, ip="192.168.2.62/24", defaultRoute=None, mac='00:00:00:00:00:0c')

    h13 = net.addHost('h13', cls=Host, ip="192.168.2.71/24", defaultRoute=None, mac='00:00:00:00:00:0d')
    h14 = net.addHost('h14', cls=Host, ip="192.168.2.72/24", defaultRoute=None, mac='00:00:00:00:00:0e')
    h15 = net.addHost('h15', cls=Host, ip="192.168.2.73/24", defaultRoute=None, mac='00:00:00:00:00:0f')

    h16 = net.addHost('h16', cls=Host, ip="192.168.2.81/24", defaultRoute=None, mac='00:00:00:00:00:10')
    h17 = net.addHost('h17', cls=Host, ip="192.168.2.82/24", defaultRoute=None, mac='00:00:00:00:00:11')
    h18 = net.addHost('h18', cls=Host, ip="192.168.2.83/24", defaultRoute=None, mac='00:00:00:00:00:12')

    h19 = net.addHost('h19', cls=Host, ip="192.168.2.91/24", defaultRoute=None, mac='00:00:00:00:00:13')
    h20 = net.addHost('h20', cls=Host, ip="192.168.2.92/24", defaultRoute=None, mac='00:00:00:00:00:14')
    h21 = net.addHost('h21', cls=Host, ip="192.168.2.93/24", defaultRoute=None, mac='00:00:00:00:00:15')

    h22 = net.addHost('h22', cls=Host, ip="192.168.2.11/24", defaultRoute=None, mac='00:00:00:00:00:16')
    h23 = net.addHost('h23', cls=Host, ip="192.168.2.12/24", defaultRoute=None, mac='00:00:00:00:00:17')
    h24 = net.addHost('h24', cls=Host, ip="192.168.2.13/24", defaultRoute=None, mac='00:00:00:00:00:18')

    info('*** Add links\n')
     # Collego gli switch tra loro
    net.addLink("s1", "s2", intfName1='s1-eth1', intfName2='s2-eth1', **http_link_config)
    net.addLink("s1", "s3", intfName1='s1-eth2', intfName2='s3-eth1', **http_link_config)
    net.addLink("s3", "s4", intfName1='s3-eth3', intfName2='s4-eth1', **http_link_config)
    net.addLink("s3", "s5", intfName1='s3-eth4', intfName2='s5-eth1', **http_link_config)
    net.addLink("s3", "s6", intfName1='s3-eth5', intfName2='s6-eth1', **http_link_config)
    net.addLink("s3", "s7", intfName1='s3-eth6', intfName2='s7-eth1', **http_link_config)
    
    # Collego gli switch agli host
    #it securety
    net.addLink("s1", "h1", intfName1='s1-eth4', intfName2='h1-eth0', **video_conf_link_config)
    net.addLink("s1", "h2", intfName1='s1-eth5', intfName2='h2-eth0', **video_conf_link_config)
    net.addLink("s1", "h3", intfName1='s1-eth6', intfName2='h3-eth0', **video_conf_link_config)
    net.addLink("s1", "h4", intfName1='s1-eth7', intfName2='h4-eth0', **video_conf_link_config)
    #conference room
    net.addLink("s1", "h5", intfName1='s1-eth8', intfName2='h5-eth0', **video_conf_link_config)
    net.addLink("s1", "h6", intfName1='s1-eth9', intfName2='h6-eth0', **video_conf_link_config)
    net.addLink("s1", "h7", intfName1='s1-eth10', intfName2='h7-eth0', **video_conf_link_config)
    net.addLink("s1", "h8", intfName1='s1-eth11', intfName2='h8-eth0', **video_conf_link_config)
    #nord office
    net.addLink("s2", "h9", intfName1='s2-eth2', intfName2='h9-eth0', **host_link_config)
    net.addLink("s2", "h10", intfName1='s2-eth3', intfName2='h10-eth0', **host_link_config)
    net.addLink("s2", "h11", intfName1='s2-eth4', intfName2='h11-eth0', **host_link_config)
    net.addLink("s2", "h12", intfName1='s2-eth5', intfName2='h12-eth0', **host_link_config)
    #ovest office
    net.addLink("s4", "h13", intfName1='s4-eth2', intfName2='h13-eth0', **host_link_config)
    net.addLink("s4", "h14", intfName1='s4-eth3', intfName2='h14-eth0', **host_link_config)
    net.addLink("s4", "h15", intfName1='s4-eth4', intfName2='h15-eth0', **host_link_config)
    net.addLink("s5", "h16", intfName1='s5-eth2', intfName2='h16-eth0', **host_link_config)
    net.addLink("s5", "h17", intfName1='s5-eth3', intfName2='h17-eth0', **host_link_config)
    net.addLink("s5", "h18", intfName1='s5-eth4', intfName2='h18-eth0', **host_link_config)
    #est office
    net.addLink("s6", "h19", intfName1='s6-eth2', intfName2='h19-eth0', **host_link_config)
    net.addLink("s6", "h20", intfName1='s6-eth3', intfName2='h20-eth0', **host_link_config)
    net.addLink("s6", "h21", intfName1='s6-eth4', intfName2='h21-eth0', **host_link_config)
    net.addLink("s7", "h22", intfName1='s7-eth2', intfName2='h22-eth0', **host_link_config)
    net.addLink("s7", "h23", intfName1='s7-eth3', intfName2='h23-eth0', **host_link_config)
    net.addLink("s7", "h24", intfName1='s7-eth4', intfName2='h24-eth0', **host_link_config)
    
    
    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])

    time.sleep(5)

    CLI(net)
    net.stop()  

if __name__ == '__main__':
    setLogLevel('info')
    runTopo()
   
