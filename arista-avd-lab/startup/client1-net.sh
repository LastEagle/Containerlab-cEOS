#!/bin/sh
set -eu

# Alpine tools (idempotent)
apk add --no-cache iproute2 busybox-extras >/dev/null 2>&1 || true

IP=/sbin/ip
[ -x "$IP" ] || IP=/usr/sbin/ip
[ -x "$IP" ] || IP=ip

# Clean up if re-running
$IP link del bond0 2>/dev/null || true

# Create LACP bond (802.3ad)
$IP link add bond0 type bond
# Force 802.3ad in sysfs (more reliable than ip args across versions)
echo 802.3ad  > /sys/class/net/bond0/bonding/mode
echo 100      > /sys/class/net/bond0/bonding/miimon
echo fast     > /sys/class/net/bond0/bonding/lacp_rate
echo layer3+4 > /sys/class/net/bond0/bonding/xmit_hash_policy

# Enslave the two links
$IP link set eth1 down || true
$IP link set eth2 down || true
$IP link set eth1 master bond0
$IP link set eth2 master bond0
$IP link set eth1 up
$IP link set eth2 up
$IP link set bond0 up

# VLAN 11
$IP link add link bond0 name bond0.11 type vlan id 11 2>/dev/null || true
$IP link set bond0.11 up
$IP addr flush dev bond0.11 || true
$IP addr add 10.10.11.11/24 dev bond0.11

# Default route via anycast gateway
$IP route replace default via 10.10.11.1

echo "=== client1 ready (VLAN 11) ==="
$IP -br addr
$IP route
cat /proc/net/bonding/bond0 2>/dev/null || true
