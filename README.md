# Containerlab-cEOS

This is a lab environment running cEOS in containerlab.  The goal is to build a EVPN-VXLAN topology with Arista AVD / Ansible for deployment.  Environment is built with Ubuntu 24.02 and docker.  

## Installation
#### Install containerlab and docker
Run this script on a clean ubuntu machine, provides everything including docker.
<pre>
curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
</pre>

#### Download the cEOS image from arista and import it to docker. I used version 4.34.0F.
<pre>
docker import cEOS-lab-4.34.0F.tar.xz ceos:4.34.0F
</pre>

#### Create containerlab python virtual-env for ansible
<pre>
python3 -m venv cvenv
</pre>
Activate the virtual-env
<pre>
source cvenv/bin/activate
</pre>


## Deploy the lab
1) Create lab in containerlab
<pre>
sudo clab deploy -t clab-topo.yml
</pre>

Switches will load with a basic start configuration from the startup folder.
2) Build EVPN-VXLAN configuration using ansible.
<pre>
ansible-playbook playbooks/build.yml
</pre>

3) Build EVPN-VXLAN configuration using ansible.
<pre>
ansible-playbook playbooks/deploy.yml
</pre>

4) Log in switches and validate.
<pre>
leaf1#sh ip bgp summary 
BGP summary information for VRF default
Router identifier 10.255.0.3, local AS number 65101
Neighbor Status Codes: m - Under maintenance
  Description              Neighbor     V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
  leaf2_Vlan4093           10.255.1.97  4 65101             21        21    0    0 00:11:43 Estab   7      7
  spine1_Ethernet3         10.255.255.0 4 65100             21        21    0    0 00:11:46 Estab   4      4
  spine2_Ethernet3         10.255.255.2 4 65100             23        21    0    0 00:11:46 Estab   4      4
</pre>


5) Validate with ansible.  Results stored in reports/
<pre>
ansible-playbook playbooks/validate.yml
</pre>


## Useful information
Default user/password for cEOS - admin//admin
Connect to cEOS
<pre>
ssh admin@clab-lab-leaf1
</pre>

Connect to linux container
<pre>
docker exec -it clab-lab-client1 sh
</pre>

Add ip address
<pre>
ip addr add 10.10.11.10/24 dev eth1
ip addr add 10.10.12.10/24 dev eth2
</pre>

disconnect form linux container
<pre>
ctrl+d
</pre>

launch containerlab
<pre>
sudo clab deploy -t clab-topo.yml
</pre>

rebuild running lab
<pre>
sudo clab deploy -t clab-topo.yml --reconfigure
</pre>

destroy lab
<pre>
sudo clab destroy -t clab-topo.yml
</pre>

Graph the lab - creates an html page at http://0.0.0.0:50080
<pre>
sudo clab graph -t clab-topo.yml
</pre>

# Preconfigured devices and mgmt interface ip address.
<pre>
╭──────────────────┬──────────────┬─────────┬────────────────╮
│       Name       │  Kind/Image  │  State  │ IPv4/6 Address │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-client1 │ linux        │ running │ 172.20.10.2    │
│                  │ alpine       │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-client2 │ linux        │ running │ 172.20.10.3    │
│                  │ alpine       │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf1   │ ceos         │ running │ 172.20.10.12   │
│                  │ ceos:4.34.0F │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf2   │ ceos         │ running │ 172.20.10.13   │
│                  │ ceos:4.34.0F │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf3   │ ceos         │ running │ 172.20.10.14   │
│                  │ ceos:4.34.0F │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf4   │ ceos         │ running │ 172.20.10.15   │
│                  │ ceos:4.34.0F │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-spine1  │ ceos         │ running │ 172.20.10.10   │
│                  │ ceos:4.34.0F │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-spine2  │ ceos         │ running │ 172.20.10.11   │
│                  │ ceos:4.34.0F │         │ N/A            │
╰──────────────────┴──────────────┴─────────┴────────────────╯
</pre>

# Containerlab setup
Config is definied in clab-topo.yml

Define your switches and hosts and ip addresses.  Managment interfaces are assigned to Managment0 in containerlab. This is definied in group_vars/DC1/dc1.yml as mgmt_interface: Management0.