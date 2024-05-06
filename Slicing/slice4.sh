#!/bin/sh

if [ -z "$1" ]
then
echo '---------- De-activating Slice 4 ----------'
fi
#coda h1
sudo ovs-vsctl set port s1-eth4 qos=@newqos -- \
    --id=@newqos create QoS type=linux-htb \
    other-config:max-rate=120000000 \
    queues:1=@1q -- \
    --id=@1q create queue other-config:min-rate=10000000 other-config:max-rate=120000000 >/dev/null
#coda h2
sudo ovs-vsctl set port s1-eth5 qos=@newqos -- \
    --id=@newqos create QoS type=linux-htb \
    other-config:max-rate=120000000 \
    queues:2=@1q -- \
    --id=@1q create queue other-config:min-rate=10000000 other-config:max-rate=120000000 >/dev/null

#coda h7
sudo ovs-vsctl set port s3-eth4 qos=@newqos -- \
    --id=@newqos create QoS type=linux-htb \
    other-config:max-rate=40000000 \
    queues:1=@1q -- \
    --id=@1q create queue other-config:min-rate=10000000 other-config:max-rate=40000000 >/dev/null
#coda h8
sudo ovs-vsctl set port s3-eth5 qos=@newqos -- \
    --id=@newqos create QoS type=linux-htb \
    other-config:max-rate=40000000 \
    queues:2=@1q -- \
    --id=@1q create queue other-config:min-rate=10000000 other-config:max-rate=40000000 >/dev/null

sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.8,idle_timeout=0,actions=set_queue:1,normal
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.7,idle_timeout=0,actions=set_queue:2,normal

sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.8,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.8,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.8,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s2 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.8,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.7,nw_dst=10.0.0.2,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s3 ip,priority=65500,nw_src=10.0.0.8,nw_dst=10.0.0.2,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.9,nw_dst=10.0.0.8,idle_timeout=0,actions=drop

sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.7,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,nw_src=10.0.0.10,nw_dst=10.0.0.8,idle_timeout=0,actions=drop
