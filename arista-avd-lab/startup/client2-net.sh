#!/bin/sh
set -eu

apk add --no-cache iproute2 busybox-extras >/dev/null 2>&1 || true

IP=/sbin/ip
[ -x "$IP" ] || IP=/usr/sbin/ip
[ -x "$IP" ] || IP=ip

$IP link del bond0 2>/dev/null || true

$IP link add bond0 type bond
echo 802.3ad  > /sys/class/net/bond0/bonding/mode
echo 100      > /sys/class/net/bond0/bonding/miimon
echo fast     > /sys/class/net/bond0/bonding/lacp_rate
echo layer3+4 > /sys/class/net/bond0/bonding/xmit_hash_policy

$IP link set eth1 down || true
$IP link set eth2 down || true
$IP link set eth1 master bond0
$IP link set eth2 master bond0
$IP link set eth1 up
$IP link set eth2 up
$IP link set bond0 up

# VLAN 21
$IP link add link bond0 name bond0.21 type vlan id 21 2>/dev/null || true
$IP link set bond0.21 up
$IP addr flush dev bond0.21 || true
$IP addr add 10.10.21.12/24 dev bond0.21

$IP route replace default via 10.10.21.1

echo "=== client2 ready (VLAN 21) ==="
$IP -br addr
$IP route
cat /proc/net/bonding/bond0 2>/dev/null || true
