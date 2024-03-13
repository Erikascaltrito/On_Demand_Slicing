#!/bin/sh

if [ -z "$1" ]
then
echo '---------- Creating Slice 1 ----------'
echo 'Switch 1:'
fi

sudo ovs-vsctl set port s1-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=5000000

if [ -z "$1" ]
then
echo 'Switch 4:'
fi
sudo ovs-vsctl set port s4-eth1 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 

if [ -z "$1" ]
then
echo '---------- End Creating Sice ----------'
fi

#flow da h1 agli altri host
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h2 agli altri host
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h3 agli altri host
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h4 agli altri host
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h5 agli altri host
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h6 agli altri host
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h7 agli altri host
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h8 agli altri host
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.9,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h9 agli altri host
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.10,idle_timeout=0,actions=drop

#flow da h10 agli altri host
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.9,idle_timeout=0,actions=drop