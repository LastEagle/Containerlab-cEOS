# Containerlab-cEOS — AVD Digital Twin Pipeline

An EVPN-VXLAN digital twin built with Arista AVD, ContainerLab, and cEOS. The pipeline spins up a full fabric, runs Batfish static config analysis, deploys intended configs, validates with ANTA, and tears down — in a single command.

```
clab-up → AVD build → Batfish → AVD deploy → ANTA validate → report → clab-down
```

**Topology:** 2 spines, 4 leaves (MLAG pairs), 3 Linux clients — EVPN-VXLAN with VRF10 and VRF11.

---

## Prerequisites

### 1. ContainerLab + Docker

Run on a clean Ubuntu 24.04 machine:

```bash
curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
```

### 2. cEOS image

Download cEOS-lab from [arista.com](https://www.arista.com/en/support/software-download) and import it:

```bash
docker import cEOS-lab-4.34.4M.tar.xz ceos:4.34.4M
```

### 3. Sudoers for ContainerLab

The pipeline runs `sudo containerlab` non-interactively. Add a sudoers entry once:

```bash
echo "netlab ALL=(ALL) NOPASSWD: /usr/bin/containerlab" | sudo tee /etc/sudoers.d/containerlab
sudo chmod 440 /etc/sudoers.d/containerlab
```

### 4. Python environment

```bash
make venv
make deps
```

This creates `arista-avd-lab/cenv/` and installs Python packages and Ansible collections (`arista.avd`, `arista.eos`).

---

## Quick Start

```bash
make pipeline
```

That's it. The pipeline handles everything: lab up, build, Batfish analysis, deploy, ANTA validation, and teardown on pass.

---

## Pipeline

### How it works

| Step | What happens |
|------|-------------|
| `clab-up` | ContainerLab deploys the topology; eAPI readiness is polled before proceeding |
| `AVD build` | `arista.avd.eos_designs` + `eos_cli_config_gen` generate intended configs |
| `Batfish` | Static analysis of configs before any device is touched |
| `AVD deploy` | `arista.avd.eos_config_deploy_eapi` pushes configs via eAPI |
| `Convergence wait` | EVPN sessions are polled until BGP prefix counts and queues stabilise |
| `ANTA validate` | `arista.avd.anta_runner` runs tests against all devices |
| `Report` | `pipeline-runs/history.json` and `pipeline-runs/latest.md` are updated |
| `clab-down` | Lab torn down on pass (configurable) |

### Makefile targets

```bash
make pipeline               # Full pipeline (default teardown: on-pass)
make pipeline-no-batfish    # Skip Batfish for quick iteration
make batfish                # Standalone Batfish only (no live lab needed — run make build first)
make pipeline TEARDOWN=never   # Keep lab running regardless of result
make pipeline TEARDOWN=always  # Always tear down
```

### pipeline.py flags

| Flag | Description |
|------|-------------|
| `--skip-clab-up` | Lab is already running |
| `--skip-build` | Skip AVD build (use existing configs in `intended/configs/`) |
| `--skip-deploy` | Skip deploy |
| `--skip-batfish` | Skip Batfish static analysis |
| `--skip-validate` | Skip ANTA validation |
| `--teardown always\|on-pass\|never` | When to destroy the lab (default: `on-pass`) |
| `--convergence-wait SECONDS` | BGP convergence polling timeout (default: 120) |

### Expected output (passing run)

```
==============================================================
  AVD Digital Twin Pipeline  [2026-03-02 15:21:19]
==============================================================
[15:22:21] [OK] ContainerLab is up.
[15:22:32] [OK] All devices ready.
[15:22:39] [OK] Build complete.
[15:22:42] [OK] Batfish static analysis PASSED — configs look clean.
[15:22:54] [OK] Deploy complete.
[15:22:55] [OK] BGP sessions converged on all devices.
[15:23:06] [OK] Phase 1: EVPN convergence — stable (queues empty, prefix counts unchanged).
[15:23:27] [OK] Phase 2: post-FIB stability — stable (queues empty, prefix counts unchanged).

==============================================================
  VALIDATION REPORT
==============================================================
[15:23:35] [  ] Total:   178
[15:23:35] [OK] Passed:  142
[15:23:35] [  ] Skipped: 36
[15:23:35] [OK] Failed:  0

==============================================================
  PIPELINE PASSED
==============================================================
```

Exit code `0` on pass, `1` on failure. The pipeline report is written to `arista-avd-lab/pipeline-runs/latest.md`.

---

## Batfish Static Analysis

[Batfish](https://batfish.org/) analyses configs without live devices, catching errors before deploy.

| Check | What it finds |
|-------|---------------|
| `initIssues` | Parse errors and unrecognised config stanzas |
| `bgpSessionCompatibility` | BGP peer mismatches (wrong AS, missing peer) |
| `undefinedReferences` | Route-maps, prefix-lists, or ACLs referenced but not defined |

Parse warnings and BGP `HALF_OPEN` sessions are expected for AVD-generated cEOS configs (Batfish EOS parser gaps and MLAG iBGP peer-groups) — they are logged as warnings and do not fail the pipeline.

Docker must be running. The pipeline starts and stops the Batfish container (`batfish/allinone`) automatically.

**Standalone analysis** (no live lab required):

```bash
make build && make batfish
```

CSV reports are written to `arista-avd-lab/batfish/reports/` after each run.

---

## ANTA Validation

Tests are run by `arista.avd.anta_runner`. Results are written to `arista-avd-lab/anta/reports/anta_report.csv`.

### Skipped tests

The following tests are not applicable in a cEOS lab environment and are skipped in `arista-avd-lab/playbooks/validate.yml`:

| Test | Reason |
|------|--------|
| `VerifyNTP` | NTP is disabled in cEOS lab |
| `VerifyInterfaceDiscards` | Management0 always has inDiscards in ContainerLab |
| `VerifyLoggingErrors` | Benign syslog errors occur during cEOS startup |
| `VerifyRunningConfigDiffs` | cEOS kernel adds `router multicast` to running-config |

---

## Lab Topology

| Node | Image | Management IP |
|------|-------|---------------|
| spine1 | ceos:4.34.4M | 172.20.10.10 |
| spine2 | ceos:4.34.4M | 172.20.10.11 |
| leaf1  | ceos:4.34.4M | 172.20.10.12 |
| leaf2  | ceos:4.34.4M | 172.20.10.13 |
| leaf3  | ceos:4.34.4M | 172.20.10.14 |
| leaf4  | ceos:4.34.4M | 172.20.10.15 |
| client1 | alpine | 172.20.10.2 |
| client2 | alpine | 172.20.10.3 |
| client3 | alpine | 172.20.10.4 |

Devices load a minimal startup config from `arista-avd-lab/startup/` on first boot (admin/admin). AVD deploys the full intended config.

---

## Manual Steps (without pipeline)

Individual Makefile targets for step-by-step control:

```bash
make clab-up           # Deploy topology
make build             # Generate AVD configs
make deploy            # Push configs to devices
make validate          # Run ANTA tests
make clab-down         # Destroy topology
make clab-reconfigure  # Reset all nodes to startup config (keeps topology, faster than reset)
make reset             # clab-down + clab-up (full teardown and redeploy)
```

---

## Useful Commands

```bash
# SSH to a cEOS device (post-deploy credentials: ansible/ansible)
ssh ansible@clab-lab-leaf1

# SSH pre-deploy (startup credentials: admin/admin)
ssh admin@clab-lab-leaf1

# Open a shell on a client container
docker exec -it clab-lab-client1 sh

# Graph the topology (opens http://0.0.0.0:50080)
sudo clab graph -t arista-avd-lab/clab-topo.yml
```
