# Containerlab-cEOS

This is a lab environment running cEOS in containerlab.  The goal is to build a EVPN-VXLAN topology with Arista AVD / Ansible for deployment.  Environment is built with Ubuntu 24.04 and docker.

## Installation
## Install containerlab and docker
Run this script on a clean ubuntu machine, provides everything including docker.
<pre>
curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
</pre>

## Download the cEOS image from arista and import it to docker. I used version 4.34.4M.
<pre>
docker import cEOS-lab-4.34.4M.tar.xz ceos:4.34.4M
</pre>

## Create the Python virtual environment
The Makefile expects the venv here: arista-avd-lab/cenv
<pre>
python3 -m venv arista-avd-lab/cenv
source arista-avd-lab/cenv/bin/activate
</pre>
<pre>
pip install -U pip
</pre>
Install Python dependencies and Ansible collections:
<pre>
pip install -r requirements.txt
ansible-galaxy collection install arista.avd arista.eos
</pre>


## Deploy the lab
1) Create lab in containerlab
<pre>
sudo clab deploy -t arista-avd-lab/clab-topo.yml
</pre>

Switches load with a basic startup configuration from arista-avd-lab/startup/.
2) Build EVPN-VXLAN configuration using ansible.
<pre>
ansible-playbook -i arista-avd-lab/inventory.yml arista-avd-lab/playbooks/build.yml
</pre>

3) Deploy the configuration (eAPI)
<pre>
ansible-playbook -i arista-avd-lab/inventory.yml arista-avd-lab/playbooks/deploy.yml
</pre>

4) Validate on a switch (example)
Log in switches and validate. (example)
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


5) Validate with Ansible
Results are stored in arista-avd-lab/reports/:
<pre>
ansible-playbook -i arista-avd-lab/inventory.yml arista-avd-lab/playbooks/validate.yml
</pre>


## Useful information
Default user/password for cEOS - admin / admin
Connect to cEOS
<pre>
ssh admin@clab-lab-leaf1
</pre>

Connect to linux container
<pre>
docker exec -it clab-lab-client1 sh
</pre>

disconnect from linux container
<pre>
ctrl+d
</pre>

launch containerlab
<pre>
sudo clab deploy -t arista-avd-lab/clab-topo.yml
</pre>

rebuild running lab
<pre>
sudo clab deploy -t arista-avd-lab/clab-topo.yml --reconfigure
</pre>

destroy lab
<pre>
sudo clab destroy -t arista-avd-lab/clab-topo.yml
</pre>

Graph the lab - creates an html page at http://0.0.0.0:50080
<pre>
sudo clab graph -t arista-avd-lab/clab-topo.yml
</pre>

# Preconfigured devices and mgmt interface ip address.
<pre>
╭──────────────────┬──────────────┬─────────┬────────────────╮
│       Name       │  Kind/Image  │  State  │ IPv4/6 Address │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-client1 │ linux        │ running │ 172.20.10.4    │
│                  │ alpine       │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-client2 │ linux        │ running │ 172.20.10.3    │
│                  │ alpine       │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-client3 │ linux        │ running │ 172.20.10.2    │
│                  │ alpine       │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf1   │ ceos         │ running │ 172.20.10.12   │
│                  │ ceos:4.34.4M │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf2   │ ceos         │ running │ 172.20.10.13   │
│                  │ ceos:4.34.4M │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf3   │ ceos         │ running │ 172.20.10.14   │
│                  │ ceos:4.34.4M │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-leaf4   │ ceos         │ running │ 172.20.10.15   │
│                  │ ceos:4.34.4M │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-spine1  │ ceos         │ running │ 172.20.10.10   │
│                  │ ceos:4.34.4M │         │ N/A            │
├──────────────────┼──────────────┼─────────┼────────────────┤
│ clab-lab-spine2  │ ceos         │ running │ 172.20.10.11   │
│                  │ ceos:4.34.4M │         │ N/A            │
╰──────────────────┴──────────────┴─────────┴────────────────╯
</pre>

# Makefile Commands
1) Bring up lab
<pre>
make clab-up
</pre>

2) Install deps (first time)
<pre>
make venv
make deps
</pre>

3) Build + deploy
<pre>
make build
make deploy
</pre>

4) Configure endpoints
<pre>
make endpoints
</pre>

5) Validate
<pre>
make validate
</pre>

6) Bring down lab
<pre>
make clab-down
</pre>

Optional: full reset
<pre>
make reset
</pre>

# Containerlab setup
Config is defined in clab-topo.yml

Define your switches and hosts and ip addresses.  Managment interfaces are assigned to Managment0 in containerlab. This is defined in group_vars/DC1/dc1.yml as mgmt_interface: Management0.