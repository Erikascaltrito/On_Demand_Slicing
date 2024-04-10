from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

import subprocess

class SlicingTopo(Topo):
    def __init__(net):
        # Initialize topology
        Topo.__init__(net)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        link_config = dict(bw=20)
        video_conf_link_config = dict(bw=20)
        host_link_config = dict(bw=10)

        # Create switch nodes
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            net.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(10):
            net.addHost("h%d" % (i + 1), **host_config)

        # Collego gli switch tra loro
        net.addLink("s1", "s2", **link_config)
        net.addLink("s1", "s3", **link_config)
        net.addLink("s1", "s4", **link_config)
        net.addLink("s2", "s3", **link_config)
        net.addLink("s3", "s4", **link_config)
        net.addLink("s2", "s4", **link_config)

        # Collego gli switch agli host
        #it securety
        net.addLink("s1", "h1", **video_conf_link_config)
        net.addLink("s1", "h2", **video_conf_link_config)
        #conference room
        net.addLink("s1", "h3", **video_conf_link_config)
        net.addLink("s1", "h4", **video_conf_link_config)
        #nord office
        net.addLink("s2", "h5", **host_link_config)
        net.addLink("s2", "h6", **host_link_config)
        #ovest office
        net.addLink("s3", "h7", **host_link_config)
        net.addLink("s3", "h8", **host_link_config)
        #est office
        net.addLink("s4", "h9", **host_link_config)
        net.addLink("s4", "h10",**host_link_config)


topos = {"networkslicingtopo": (lambda: SlicingTopo())}

if __name__ == "__main__":
    topo = SlicingTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    
    setLogLevel("info") 
    
    controller = RemoteController("c0", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()

    subprocess.call("Slicing/./total_activity.sh")

    CLI(net)
    net.stop()
