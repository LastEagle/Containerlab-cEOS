# Validate State Report

**Table of Contents:**

- [Validate State Report](validate-state-report)
  - [Test Results Summary](#test-results-summary)
  - [Failed Test Results Summary](#failed-test-results-summary)
  - [All Test Results](#all-test-results)

## Test Results Summary

### Summary Totals

| Total Tests | Total Tests Passed | Total Tests Failed | Total Tests Skipped |
| ----------- | ------------------ | ------------------ | ------------------- |
| 228 | 194 | 10 | 24 |

### Summary Totals Device Under Test

| Device Under Test | Total Tests | Tests Passed | Tests Failed | Tests Skipped | Categories Failed | Categories Skipped |
| ------------------| ----------- | ------------ | ------------ | ------------- | ----------------- | ------------------ |
| leaf1 | 43 | 37 | 2 | 4 | Interfaces, System | Hardware |
| leaf2 | 43 | 37 | 2 | 4 | Interfaces, System | Hardware |
| leaf3 | 43 | 37 | 2 | 4 | Interfaces, System | Hardware |
| leaf4 | 43 | 37 | 2 | 4 | Interfaces, System | Hardware |
| spine1 | 28 | 23 | 1 | 4 | System | Hardware |
| spine2 | 28 | 23 | 1 | 4 | System | Hardware |

### Summary Totals Per Category

| Test Category | Total Tests | Tests Passed | Tests Failed | Tests Skipped |
| ------------- | ----------- | ------------ | ------------ | ------------- |
| BGP | 36 | 36 | 0 | 0 |
| Connectivity | 64 | 64 | 0 | 0 |
| Hardware | 24 | 0 | 0 | 24 |
| Interfaces | 50 | 46 | 4 | 0 |
| MLAG | 4 | 4 | 0 | 0 |
| Routing | 38 | 38 | 0 | 0 |
| System | 12 | 6 | 6 | 0 |

## Failed Test Results Summary

| ID | Device Under Test | Categories | Test | Description | Inputs | Result | Messages |
| -- | ----------------- | ---------- | ---- | ----------- | ------ | -------| -------- |
| 31 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 42 | leaf1 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 74 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 85 | leaf2 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 117 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 128 | leaf3 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 160 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 171 | leaf4 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 199 | spine1 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 227 | spine2 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |

## All Test Results

| ID | Device Under Test | Categories | Test | Description | Inputs | Result | Messages |
| -- | ----------------- | ---------- | ---- | ----------- | ------ | -------| -------- |
| 1 | leaf1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine1 (IP: 10.255.0.1) | PASS | - |
| 2 | leaf1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine2 (IP: 10.255.0.2) | PASS | - |
| 3 | leaf1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf2 (IP: 10.255.1.97) | PASS | - |
| 4 | leaf1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine1 (IP: 10.255.255.0) | PASS | - |
| 5 | leaf1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine2 (IP: 10.255.255.2) | PASS | - |
| 6 | leaf1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet10 - Remote: spine1 Ethernet3 | PASS | - |
| 7 | leaf1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet11 - Remote: spine2 Ethernet3 | PASS | - |
| 8 | leaf1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet8 - Remote: leaf2 Ethernet8 | PASS | - |
| 9 | leaf1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet9 - Remote: leaf2 Ethernet9 | PASS | - |
| 10 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.3) - Destination: leaf1 Loopback0 (IP: 10.255.0.3) | PASS | - |
| 11 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.3) - Destination: leaf2 Loopback0 (IP: 10.255.0.4) | PASS | - |
| 12 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.3) - Destination: leaf3 Loopback0 (IP: 10.255.0.5) | PASS | - |
| 13 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.3) - Destination: leaf4 Loopback0 (IP: 10.255.0.6) | PASS | - |
| 14 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.3) - Destination: spine1 Loopback0 (IP: 10.255.0.1) | PASS | - |
| 15 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.3) - Destination: spine2 Loopback0 (IP: 10.255.0.2) | PASS | - |
| 16 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet10 (IP: 10.255.255.1) - Destination: spine1 Ethernet3 (IP: 10.255.255.0) | PASS | - |
| 17 | leaf1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet11 (IP: 10.255.255.3) - Destination: spine2 Ethernet3 (IP: 10.255.255.2) | PASS | - |
| 18 | leaf1 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab |
| 19 | leaf1 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab |
| 20 | leaf1 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab |
| 21 | leaf1 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab |
| 22 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet10 - P2P_spine1_Ethernet3 = 'up' | PASS | - |
| 23 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet11 - P2P_spine2_Ethernet3 = 'up' | PASS | - |
| 24 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet8 - MLAG_leaf2_Ethernet8 = 'up' | PASS | - |
| 25 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet9 - MLAG_leaf2_Ethernet9 = 'up' | PASS | - |
| 26 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback0 - ROUTER_ID = 'up' | PASS | - |
| 27 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback1 - VXLAN_TUNNEL_SOURCE = 'up' | PASS | - |
| 28 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Port-Channel8 - MLAG_leaf2_Port-Channel8 = 'up' | PASS | - |
| 29 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 30 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 31 | leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 32 | leaf1 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 33 | leaf1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 34 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.1 - Peer: spine1 | PASS | - |
| 35 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.2 - Peer: spine2 | PASS | - |
| 36 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.3 - Peer: leaf1 | PASS | - |
| 37 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.4 - Peer: leaf2 | PASS | - |
| 38 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.5 - Peer: leaf3 | PASS | - |
| 39 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.6 - Peer: leaf4 | PASS | - |
| 40 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.3 - Peer: leaf1 | PASS | - |
| 41 | leaf1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.5 - Peer: leaf3 | PASS | - |
| 42 | leaf1 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 43 | leaf1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 44 | leaf2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine1 (IP: 10.255.0.1) | PASS | - |
| 45 | leaf2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine2 (IP: 10.255.0.2) | PASS | - |
| 46 | leaf2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf1 (IP: 10.255.1.96) | PASS | - |
| 47 | leaf2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine1 (IP: 10.255.255.4) | PASS | - |
| 48 | leaf2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine2 (IP: 10.255.255.6) | PASS | - |
| 49 | leaf2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet10 - Remote: spine1 Ethernet4 | PASS | - |
| 50 | leaf2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet11 - Remote: spine2 Ethernet4 | PASS | - |
| 51 | leaf2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet8 - Remote: leaf1 Ethernet8 | PASS | - |
| 52 | leaf2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet9 - Remote: leaf1 Ethernet9 | PASS | - |
| 53 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.4) - Destination: leaf1 Loopback0 (IP: 10.255.0.3) | PASS | - |
| 54 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.4) - Destination: leaf2 Loopback0 (IP: 10.255.0.4) | PASS | - |
| 55 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.4) - Destination: leaf3 Loopback0 (IP: 10.255.0.5) | PASS | - |
| 56 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.4) - Destination: leaf4 Loopback0 (IP: 10.255.0.6) | PASS | - |
| 57 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.4) - Destination: spine1 Loopback0 (IP: 10.255.0.1) | PASS | - |
| 58 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.4) - Destination: spine2 Loopback0 (IP: 10.255.0.2) | PASS | - |
| 59 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet10 (IP: 10.255.255.5) - Destination: spine1 Ethernet4 (IP: 10.255.255.4) | PASS | - |
| 60 | leaf2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet11 (IP: 10.255.255.7) - Destination: spine2 Ethernet4 (IP: 10.255.255.6) | PASS | - |
| 61 | leaf2 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab |
| 62 | leaf2 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab |
| 63 | leaf2 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab |
| 64 | leaf2 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab |
| 65 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet10 - P2P_spine1_Ethernet4 = 'up' | PASS | - |
| 66 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet11 - P2P_spine2_Ethernet4 = 'up' | PASS | - |
| 67 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet8 - MLAG_leaf1_Ethernet8 = 'up' | PASS | - |
| 68 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet9 - MLAG_leaf1_Ethernet9 = 'up' | PASS | - |
| 69 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback0 - ROUTER_ID = 'up' | PASS | - |
| 70 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback1 - VXLAN_TUNNEL_SOURCE = 'up' | PASS | - |
| 71 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Port-Channel8 - MLAG_leaf1_Port-Channel8 = 'up' | PASS | - |
| 72 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 73 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 74 | leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 75 | leaf2 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 76 | leaf2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 77 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.1 - Peer: spine1 | PASS | - |
| 78 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.2 - Peer: spine2 | PASS | - |
| 79 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.3 - Peer: leaf1 | PASS | - |
| 80 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.4 - Peer: leaf2 | PASS | - |
| 81 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.5 - Peer: leaf3 | PASS | - |
| 82 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.6 - Peer: leaf4 | PASS | - |
| 83 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.3 - Peer: leaf1 | PASS | - |
| 84 | leaf2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.5 - Peer: leaf3 | PASS | - |
| 85 | leaf2 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 86 | leaf2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 87 | leaf3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine1 (IP: 10.255.0.1) | PASS | - |
| 88 | leaf3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine2 (IP: 10.255.0.2) | PASS | - |
| 89 | leaf3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf4 (IP: 10.255.1.101) | PASS | - |
| 90 | leaf3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine1 (IP: 10.255.255.8) | PASS | - |
| 91 | leaf3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine2 (IP: 10.255.255.10) | PASS | - |
| 92 | leaf3 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet10 - Remote: spine1 Ethernet5 | PASS | - |
| 93 | leaf3 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet11 - Remote: spine2 Ethernet5 | PASS | - |
| 94 | leaf3 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet8 - Remote: leaf4 Ethernet8 | PASS | - |
| 95 | leaf3 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet9 - Remote: leaf4 Ethernet9 | PASS | - |
| 96 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.5) - Destination: leaf1 Loopback0 (IP: 10.255.0.3) | PASS | - |
| 97 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.5) - Destination: leaf2 Loopback0 (IP: 10.255.0.4) | PASS | - |
| 98 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.5) - Destination: leaf3 Loopback0 (IP: 10.255.0.5) | PASS | - |
| 99 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.5) - Destination: leaf4 Loopback0 (IP: 10.255.0.6) | PASS | - |
| 100 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.5) - Destination: spine1 Loopback0 (IP: 10.255.0.1) | PASS | - |
| 101 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.5) - Destination: spine2 Loopback0 (IP: 10.255.0.2) | PASS | - |
| 102 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet10 (IP: 10.255.255.9) - Destination: spine1 Ethernet5 (IP: 10.255.255.8) | PASS | - |
| 103 | leaf3 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet11 (IP: 10.255.255.11) - Destination: spine2 Ethernet5 (IP: 10.255.255.10) | PASS | - |
| 104 | leaf3 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab |
| 105 | leaf3 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab |
| 106 | leaf3 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab |
| 107 | leaf3 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab |
| 108 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet10 - P2P_spine1_Ethernet5 = 'up' | PASS | - |
| 109 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet11 - P2P_spine2_Ethernet5 = 'up' | PASS | - |
| 110 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet8 - MLAG_leaf4_Ethernet8 = 'up' | PASS | - |
| 111 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet9 - MLAG_leaf4_Ethernet9 = 'up' | PASS | - |
| 112 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback0 - ROUTER_ID = 'up' | PASS | - |
| 113 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback1 - VXLAN_TUNNEL_SOURCE = 'up' | PASS | - |
| 114 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Port-Channel8 - MLAG_leaf4_Port-Channel8 = 'up' | PASS | - |
| 115 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 116 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 117 | leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 118 | leaf3 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 119 | leaf3 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 120 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.1 - Peer: spine1 | PASS | - |
| 121 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.2 - Peer: spine2 | PASS | - |
| 122 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.3 - Peer: leaf1 | PASS | - |
| 123 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.4 - Peer: leaf2 | PASS | - |
| 124 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.5 - Peer: leaf3 | PASS | - |
| 125 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.6 - Peer: leaf4 | PASS | - |
| 126 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.3 - Peer: leaf1 | PASS | - |
| 127 | leaf3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.5 - Peer: leaf3 | PASS | - |
| 128 | leaf3 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 129 | leaf3 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 130 | leaf4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine1 (IP: 10.255.0.1) | PASS | - |
| 131 | leaf4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: spine2 (IP: 10.255.0.2) | PASS | - |
| 132 | leaf4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf3 (IP: 10.255.1.100) | PASS | - |
| 133 | leaf4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine1 (IP: 10.255.255.12) | PASS | - |
| 134 | leaf4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: spine2 (IP: 10.255.255.14) | PASS | - |
| 135 | leaf4 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet10 - Remote: spine1 Ethernet6 | PASS | - |
| 136 | leaf4 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet11 - Remote: spine2 Ethernet6 | PASS | - |
| 137 | leaf4 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet8 - Remote: leaf3 Ethernet8 | PASS | - |
| 138 | leaf4 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet9 - Remote: leaf3 Ethernet9 | PASS | - |
| 139 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.6) - Destination: leaf1 Loopback0 (IP: 10.255.0.3) | PASS | - |
| 140 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.6) - Destination: leaf2 Loopback0 (IP: 10.255.0.4) | PASS | - |
| 141 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.6) - Destination: leaf3 Loopback0 (IP: 10.255.0.5) | PASS | - |
| 142 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.6) - Destination: leaf4 Loopback0 (IP: 10.255.0.6) | PASS | - |
| 143 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.6) - Destination: spine1 Loopback0 (IP: 10.255.0.1) | PASS | - |
| 144 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 10.255.0.6) - Destination: spine2 Loopback0 (IP: 10.255.0.2) | PASS | - |
| 145 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet10 (IP: 10.255.255.13) - Destination: spine1 Ethernet6 (IP: 10.255.255.12) | PASS | - |
| 146 | leaf4 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet11 (IP: 10.255.255.15) - Destination: spine2 Ethernet6 (IP: 10.255.255.14) | PASS | - |
| 147 | leaf4 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab |
| 148 | leaf4 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab |
| 149 | leaf4 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab |
| 150 | leaf4 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab |
| 151 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet10 - P2P_spine1_Ethernet6 = 'up' | PASS | - |
| 152 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet11 - P2P_spine2_Ethernet6 = 'up' | PASS | - |
| 153 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet8 - MLAG_leaf3_Ethernet8 = 'up' | PASS | - |
| 154 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet9 - MLAG_leaf3_Ethernet9 = 'up' | PASS | - |
| 155 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback0 - ROUTER_ID = 'up' | PASS | - |
| 156 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback1 - VXLAN_TUNNEL_SOURCE = 'up' | PASS | - |
| 157 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Port-Channel8 - MLAG_leaf3_Port-Channel8 = 'up' | PASS | - |
| 158 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 159 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 160 | leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Vxlan1 = 'up' | FAIL | Vxlan1 - Status mismatch - Expected: up/up, Actual: down/down |
| 161 | leaf4 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 162 | leaf4 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 163 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.1 - Peer: spine1 | PASS | - |
| 164 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.2 - Peer: spine2 | PASS | - |
| 165 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.3 - Peer: leaf1 | PASS | - |
| 166 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.4 - Peer: leaf2 | PASS | - |
| 167 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.5 - Peer: leaf3 | PASS | - |
| 168 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.0.6 - Peer: leaf4 | PASS | - |
| 169 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.3 - Peer: leaf1 | PASS | - |
| 170 | leaf4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 10.255.1.5 - Peer: leaf3 | PASS | - |
| 171 | leaf4 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 172 | leaf4 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 173 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf1 (IP: 10.255.0.3) | PASS | - |
| 174 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf2 (IP: 10.255.0.4) | PASS | - |
| 175 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf3 (IP: 10.255.0.5) | PASS | - |
| 176 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf4 (IP: 10.255.0.6) | PASS | - |
| 177 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf1 (IP: 10.255.255.1) | PASS | - |
| 178 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf2 (IP: 10.255.255.5) | PASS | - |
| 179 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf3 (IP: 10.255.255.9) | PASS | - |
| 180 | spine1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf4 (IP: 10.255.255.13) | PASS | - |
| 181 | spine1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet3 - Remote: leaf1 Ethernet10 | PASS | - |
| 182 | spine1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet4 - Remote: leaf2 Ethernet10 | PASS | - |
| 183 | spine1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet5 - Remote: leaf3 Ethernet10 | PASS | - |
| 184 | spine1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet6 - Remote: leaf4 Ethernet10 | PASS | - |
| 185 | spine1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 10.255.255.0) - Destination: leaf1 Ethernet10 (IP: 10.255.255.1) | PASS | - |
| 186 | spine1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 10.255.255.4) - Destination: leaf2 Ethernet10 (IP: 10.255.255.5) | PASS | - |
| 187 | spine1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet5 (IP: 10.255.255.8) - Destination: leaf3 Ethernet10 (IP: 10.255.255.9) | PASS | - |
| 188 | spine1 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet6 (IP: 10.255.255.12) - Destination: leaf4 Ethernet10 (IP: 10.255.255.13) | PASS | - |
| 189 | spine1 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab |
| 190 | spine1 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab |
| 191 | spine1 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab |
| 192 | spine1 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab |
| 193 | spine1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet3 - P2P_leaf1_Ethernet10 = 'up' | PASS | - |
| 194 | spine1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet4 - P2P_leaf2_Ethernet10 = 'up' | PASS | - |
| 195 | spine1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet5 - P2P_leaf3_Ethernet10 = 'up' | PASS | - |
| 196 | spine1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet6 - P2P_leaf4_Ethernet10 = 'up' | PASS | - |
| 197 | spine1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback0 - ROUTER_ID = 'up' | PASS | - |
| 198 | spine1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 199 | spine1 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 200 | spine1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 201 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf1 (IP: 10.255.0.3) | PASS | - |
| 202 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf2 (IP: 10.255.0.4) | PASS | - |
| 203 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf3 (IP: 10.255.0.5) | PASS | - |
| 204 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP EVPN Peer: leaf4 (IP: 10.255.0.6) | PASS | - |
| 205 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf1 (IP: 10.255.255.3) | PASS | - |
| 206 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf2 (IP: 10.255.255.7) | PASS | - |
| 207 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf3 (IP: 10.255.255.11) | PASS | - |
| 208 | spine2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s) for given address families. | BGP IPv4 Unicast Peer: leaf4 (IP: 10.255.255.15) | PASS | - |
| 209 | spine2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet3 - Remote: leaf1 Ethernet11 | PASS | - |
| 210 | spine2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet4 - Remote: leaf2 Ethernet11 | PASS | - |
| 211 | spine2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet5 - Remote: leaf3 Ethernet11 | PASS | - |
| 212 | spine2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | Local: Ethernet6 - Remote: leaf4 Ethernet11 | PASS | - |
| 213 | spine2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 10.255.255.2) - Destination: leaf1 Ethernet11 (IP: 10.255.255.3) | PASS | - |
| 214 | spine2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 10.255.255.6) - Destination: leaf2 Ethernet11 (IP: 10.255.255.7) | PASS | - |
| 215 | spine2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet5 (IP: 10.255.255.10) - Destination: leaf3 Ethernet11 (IP: 10.255.255.11) | PASS | - |
| 216 | spine2 | Connectivity | VerifyReachability | Test network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet6 (IP: 10.255.255.14) - Destination: leaf4 Ethernet11 (IP: 10.255.255.15) | PASS | - |
| 217 | spine2 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab |
| 218 | spine2 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab |
| 219 | spine2 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab |
| 220 | spine2 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab |
| 221 | spine2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet3 - P2P_leaf1_Ethernet11 = 'up' | PASS | - |
| 222 | spine2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet4 - P2P_leaf2_Ethernet11 = 'up' | PASS | - |
| 223 | spine2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet5 - P2P_leaf3_Ethernet11 = 'up' | PASS | - |
| 224 | spine2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Ethernet6 - P2P_leaf4_Ethernet11 = 'up' | PASS | - |
| 225 | spine2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Interface Loopback0 - ROUTER_ID = 'up' | PASS | - |
| 226 | spine2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 227 | spine2 | System | VerifyNTP | Verifies if NTP is synchronised. | - | FAIL | NTP status mismatch - Expected: synchronised Actual: NTP is disabled. |
| 228 | spine2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
