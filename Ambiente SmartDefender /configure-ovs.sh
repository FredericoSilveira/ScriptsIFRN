#!/bin/bash

#COLLECTOR_IP=172.16.20.155,172.16.20.156,172.16.20.157,172.16.20.111
#COLLECTOR_IP=10.13.98.129,172.16.20.157
#COLLECTOR_IP=172.16.20.157
COLLECTOR_IP=10.7.40.196
#COLLECTOR_IP=10.13.98.129
COLLECTOR_PORT=6343
AGENT_IP=127.0.0.1
HEADER_BYTES=128
SAMPLING_N=$1
POLLING_SECS=30
EXTERNAL_IFACE="eth0"
EXTERNAL_BRIDGE="sw0"
LOCAL_IFACE="eth1"
LOCAL_BRIDGE="sw1"

# Configure Bridge INTERNAL BR

ip addr flush dev $LOCAL_IFACE
ovs-vsctl --may-exist add-br $LOCAL_BRIDGE
ovs-vsctl --may-exist add-port $LOCAL_BRIDGE $LOCAL_IFACE
ip addr add 169.254.0.154/16 scope host dev $LOCAL_BRIDGE
ip link set $LOCAL_IFACE up
ip link set $LOCAL_BRIDGE up
ip link set mtu 3000 dev $LOCAL_IFACE

# Configure External BR

ip addr flush dev $EXTERNAL_IFACE
ovs-vsctl --may-exist add-br $EXTERNAL_BRIDGE
ovs-vsctl --may-exist add-port $EXTERNAL_BRIDGE $EXTERNAL_IFACE
ip addr add 172.16.20.154/24 dev $EXTERNAL_BRIDGE
ip link set $EXTERNAL_IFACE up
ip link set $EXTERNAL_BRIDGE up
ip route add default via 172.16.20.1

ovs-vsctl -- --id=@sflow create sflow agent=${AGENT_IP} target=${COLLECTOR_IP} header=${HEADER_BYTES} sampling=${SAMPLING_N}\
        polling=${POLLING_SECS} -- set bridge $LOCAL_BRIDGE sflow=@sflow