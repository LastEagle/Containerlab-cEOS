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

# Pipeline Orchestrator (pipeline.py)

`pipeline.py` automates the full digital twin workflow in a single command:

```
clab-up → AVD build → Batfish static analysis → AVD deploy → ANTA validate → report → clab-down
```

The lab is torn down automatically on a passing run. On failure it is left running so you can inspect the devices.

## Prerequisites

`containerlab` must be allowed to run without a password prompt. Add a sudoers entry once:
<pre>
echo "netlab ALL=(ALL) NOPASSWD: /usr/bin/containerlab" | sudo tee /etc/sudoers.d/containerlab
sudo chmod 440 /etc/sudoers.d/containerlab
</pre>

## Running the pipeline

Full run (spin up lab, build, deploy, validate, tear down on pass):
<pre>
python3 pipeline.py
</pre>

Or via Make:
<pre>
make pipeline
</pre>

## Options

| Flag | Description |
|------|-------------|
| `--skip-clab-up` | Skip ContainerLab deploy (use when lab is already running) |
| `--skip-build` | Skip AVD build step |
| `--skip-deploy` | Skip AVD deploy step |
| `--skip-batfish` | Skip Batfish static analysis |
| `--skip-validate` | Skip ANTA validation and result parsing |
| `--teardown always\|on-pass\|never` | Control when the lab is torn down (default: `on-pass`) |

Examples:
<pre>
# Full pipeline (Batfish runs by default)
python3 pipeline.py

# Skip Batfish for a quick iteration
python3 pipeline.py --skip-batfish

# Lab already running — just build, Batfish, deploy, validate
python3 pipeline.py --skip-clab-up

# Keep lab running regardless of result (useful for debugging)
python3 pipeline.py --teardown never

# Makefile: keep lab running
make pipeline TEARDOWN=never

# Makefile: skip Batfish
make pipeline-no-batfish
</pre>

## Expected output

A passing run looks like:
<pre>
==============================================================
  AVD Digital Twin Pipeline  [2026-03-02 14:38:31]
==============================================================
[14:38:31] [>>] Deploying topology...
[14:39:43] [OK] All devices ready.
[14:39:50] [OK] Build complete.
[14:39:52] [OK] Batfish static analysis PASSED — configs look clean.
[14:40:04] [OK] Deploy complete.
[14:40:05] [OK] BGP sessions converged on all devices.
[14:40:28] [OK] Validation playbook complete.

==============================================================
  VALIDATION REPORT
==============================================================
[14:40:28] [  ] Total:   184
[14:40:28] [OK] Passed:  148
[14:40:28] [  ] Skipped: 36
[14:40:28] [OK] Failed:  0

==============================================================
  PIPELINE PASSED
==============================================================
</pre>

Exit code is `0` on pass, `1` on failure.

## Skipped tests (cEOS lab)

The following tests are not applicable in a cEOS lab environment and are skipped via `avd_catalogs_filters` in `arista-avd-lab/playbooks/validate.yml`. They will not appear as failures in the report.

| Test | Reason |
|------|--------|
| `VerifyNTP` | NTP is disabled in cEOS lab |
| `VerifyInterfaceDiscards` | Management0 always has inDiscards in containerlab (management port discards multicast/broadcast) |
| `VerifyLoggingErrors` | Benign syslog errors occur during cEOS container startup |

To add more skipped tests, add them to the `skip_tests` list under `avd_catalogs_filters` in `validate.yml`.

Results are written to `arista-avd-lab/anta/reports/anta_report.csv` after each validate run.

# Batfish Static Config Analysis

[Batfish](https://batfish.org/) performs vendor-agnostic static analysis of network device configurations without requiring live devices. In this pipeline it runs **between build and deploy** and can catch issues before any config touches a switch.

## What it checks

| Check | What it finds |
|-------|---------------|
| `initIssues` | Parse errors and unrecognised config stanzas |
| `bgpSessionCompatibility` | Mismatched BGP peer config (wrong AS, missing peer, etc.) |
| `undefinedReferences` | Route-maps, prefix-lists, or ACLs referenced but never defined |

BGP `HALF_OPEN` sessions (MLAG iBGP peer-groups without a matching remote config in the snapshot) are reported as warnings, not failures, because the peer side is not included in the Batfish snapshot.

## Prerequisites

Install the Python client (included in `requirements.txt`, installed via `make deps`):

<pre>
make deps
</pre>

Docker must be running — the pipeline starts and stops the Batfish container automatically. No manual `docker run` required.

## Usage

**Full pipeline** — Batfish runs by default between build and deploy:

<pre>
make pipeline
</pre>

**Skip Batfish** for a quick iteration:

<pre>
make pipeline-no-batfish
</pre>

**Standalone lab-free analysis** (build configs first, then analyse without spinning up cEOS):

<pre>
make build && make batfish
</pre>

## Flags

| Flag | Description |
|------|-------------|
| `--skip-batfish` | Skip Batfish static analysis |
| `--skip-validate` | Skip ANTA validation and result parsing |

## Expected output (passing)

<pre>
==============================================================
  Batfish — Starting container
==============================================================
[14:39:50] [  ] Starting Batfish container (batfish/allinone)...
[14:39:55] [OK] Batfish container ready.

==============================================================
  STEP 2b: Batfish — Static Config Analysis
==============================================================
[14:39:55] [  ] Batfish reachable. Staging 6 config(s) for snapshot upload...
[14:39:56] [  ] Snapshot loaded from: .../intended/configs
[14:39:56] [>>] Querying Batfish (initIssues, bgpSessionCompatibility, undefinedReferences)...
[14:39:56] [~~] initIssues: 122 parse warning(s) — unrecognised EOS syntax (expected for cEOS).
[14:39:56] [~~] bgpSessionCompatibility: 16 session(s) with expected cEOS/MLAG limitations.
[14:39:56] [OK] undefinedReferences: no non-BGP undefined references found.
[14:39:56] [OK] Batfish static analysis PASSED — configs look clean.
</pre>

The parse warnings and BGP limitations are expected for cEOS AVD configs — they are Batfish parser gaps with EOS syntax, not real config errors. The pipeline only fails on genuine issues: non-BGP undefined references (missing route-maps, prefix-lists) or unexpected BGP session mismatches.

CSV reports are written to `arista-avd-lab/batfish/reports/` after each run.

# Containerlab setup
Config is defined in clab-topo.yml

Define your switches and hosts and ip addresses.  Managment interfaces are assigned to Managment0 in containerlab. This is defined in group_vars/DC1/dc1.yml as mgmt_interface: Management0.