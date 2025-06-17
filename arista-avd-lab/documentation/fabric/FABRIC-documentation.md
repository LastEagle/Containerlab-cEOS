# FABRIC

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| FABRIC | l3leaf | leaf1 | 172.20.10.12/24 | cEOS-lab | Provisioned | - |
| FABRIC | l3leaf | leaf2 | 172.20.10.13/24 | cEOS-lab | Provisioned | - |
| FABRIC | l3leaf | leaf3 | 172.20.10.14/24 | cEOS-lab | Provisioned | - |
| FABRIC | l3leaf | leaf4 | 172.20.10.15/24 | cEOS-lab | Provisioned | - |
| FABRIC | spine | spine1 | 172.20.10.10/24 | cEOS-lab | Provisioned | - |
| FABRIC | spine | spine2 | 172.20.10.11/24 | cEOS-lab | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l3leaf | leaf1 | Ethernet8 | mlag_peer | leaf2 | Ethernet8 |
| l3leaf | leaf1 | Ethernet9 | mlag_peer | leaf2 | Ethernet9 |
| l3leaf | leaf1 | Ethernet10 | spine | spine1 | Ethernet3 |
| l3leaf | leaf1 | Ethernet11 | spine | spine2 | Ethernet3 |
| l3leaf | leaf2 | Ethernet10 | spine | spine1 | Ethernet4 |
| l3leaf | leaf2 | Ethernet11 | spine | spine2 | Ethernet4 |
| l3leaf | leaf3 | Ethernet8 | mlag_peer | leaf4 | Ethernet8 |
| l3leaf | leaf3 | Ethernet9 | mlag_peer | leaf4 | Ethernet9 |
| l3leaf | leaf3 | Ethernet10 | spine | spine1 | Ethernet5 |
| l3leaf | leaf3 | Ethernet11 | spine | spine2 | Ethernet5 |
| l3leaf | leaf4 | Ethernet10 | spine | spine1 | Ethernet6 |
| l3leaf | leaf4 | Ethernet11 | spine | spine2 | Ethernet6 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 10.255.255.0/26 | 64 | 16 | 25.0 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| leaf1 | Ethernet10 | 10.255.255.1/31 | spine1 | Ethernet3 | 10.255.255.0/31 |
| leaf1 | Ethernet11 | 10.255.255.3/31 | spine2 | Ethernet3 | 10.255.255.2/31 |
| leaf2 | Ethernet10 | 10.255.255.5/31 | spine1 | Ethernet4 | 10.255.255.4/31 |
| leaf2 | Ethernet11 | 10.255.255.7/31 | spine2 | Ethernet4 | 10.255.255.6/31 |
| leaf3 | Ethernet10 | 10.255.255.9/31 | spine1 | Ethernet5 | 10.255.255.8/31 |
| leaf3 | Ethernet11 | 10.255.255.11/31 | spine2 | Ethernet5 | 10.255.255.10/31 |
| leaf4 | Ethernet10 | 10.255.255.13/31 | spine1 | Ethernet6 | 10.255.255.12/31 |
| leaf4 | Ethernet11 | 10.255.255.15/31 | spine2 | Ethernet6 | 10.255.255.14/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 10.255.0.0/27 | 32 | 6 | 18.75 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| FABRIC | leaf1 | 10.255.0.3/32 |
| FABRIC | leaf2 | 10.255.0.4/32 |
| FABRIC | leaf3 | 10.255.0.5/32 |
| FABRIC | leaf4 | 10.255.0.6/32 |
| FABRIC | spine1 | 10.255.0.1/32 |
| FABRIC | spine2 | 10.255.0.2/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |
| 10.255.1.0/27 | 32 | 4 | 12.5 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| FABRIC | leaf1 | 10.255.1.3/32 |
| FABRIC | leaf2 | 10.255.1.3/32 |
| FABRIC | leaf3 | 10.255.1.5/32 |
| FABRIC | leaf4 | 10.255.1.5/32 |
