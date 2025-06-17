# Containerlab-cEOS

Default user/password for cEOS - ansible//ansible
Connect to cEOS
<pre>
ssh ansible@clab-lab-leaf1
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