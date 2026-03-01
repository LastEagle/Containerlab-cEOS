#!/bin/sh
set -eu

apk add --no-cache iproute2 >/dev/null 2>&1 || true
modprobe bonding 2>/dev/null || true

# Create LACP bond (802.3ad)
ip link add bond0 type bond mode 802.3ad miimon 100 lacp_rate fast xmit_hash_policy layer3+4 2>/dev/null || true

ip link set eth1 down || true
ip link set eth2 down || true
ip link set eth1 master bond0 || true
ip link set eth2 master bond0 || true
ip link set eth1 up || true
ip link set eth2 up || true
ip link set bond0 up || true

# VLAN 11 interface
ip link add link bond0 name bond0.11 type vlan id 11 2>/dev/null || true
ip link set bond0.11 up || true

# IP for client3 in VLAN 11
ip addr flush dev bond0.11 2>/dev/null || true
ip addr add 10.10.11.12/24 dev bond0.11

# Default route via anycast SVI
ip route replace default via 10.10.11.1

# Quick visibility
ip -br addr
ip route
cat /proc/net/bonding/bond0 2>/dev/null || true
