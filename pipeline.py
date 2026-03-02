#!/usr/bin/env python3
"""
AVD ContainerLab Pipeline Orchestrator
Flow: clab-up → build → [batfish] → deploy → validate → report → clab-down (conditional)
"""

import argparse
import base64
import csv
import json
import shutil
import signal
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.request
import yaml
from datetime import datetime
from pathlib import Path

REPO_ROOT     = Path(__file__).parent
LAB_DIR       = REPO_ROOT / "arista-avd-lab"
TOPO          = LAB_DIR / "clab-topo.yml"
VENV_ACTIVATE = LAB_DIR / "cenv" / "bin" / "activate"
RESULTS_CSV   = LAB_DIR / "anta" / "reports" / "anta_report.csv"
FABRIC_VARS   = LAB_DIR / "group_vars" / "FABRIC" / "fabric.yml"
CONFIGS_DIR        = LAB_DIR / "intended" / "configs"
BATFISH_REPORT_DIR = LAB_DIR / "batfish" / "reports"
PIPELINE_RUNS_DIR  = LAB_DIR / "pipeline-runs"
HISTORY_JSON       = PIPELINE_RUNS_DIR / "history.json"
LATEST_MD          = PIPELINE_RUNS_DIR / "latest.md"

BUILD_PLAY    = Path("playbooks/build.yml")
DEPLOY_PLAY   = Path("playbooks/deploy.yml")
VALIDATE_PLAY = Path("playbooks/validate.yml")
INVENTORY     = Path("inventory.yml")


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

ICONS = {"INFO": "  ", "STEP": ">>", "PASS": "OK", "FAIL": "!!", "WARN": "~~"}


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    icon = ICONS.get(level, "  ")
    print(f"[{ts}] [{icon}] {msg}", flush=True)


def banner(title: str):
    width = 62
    print(f"\n{'=' * width}\n  {title}\n{'=' * width}")


# ---------------------------------------------------------------------------
# Command runner
# ---------------------------------------------------------------------------

def run(cmd: list, use_venv: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command, optionally inside the lab venv. Always runs from LAB_DIR."""
    if use_venv:
        cmd_str = f". {VENV_ACTIVATE} && " + " ".join(str(c) for c in cmd)
        return subprocess.run(
            cmd_str, shell=True, executable="/bin/bash",
            cwd=LAB_DIR, check=check,
        )
    return subprocess.run(cmd, check=check, cwd=LAB_DIR)


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def clab_up():
    banner("STEP 1: ContainerLab — deploy")
    log("Deploying topology...", "STEP")
    run(["sudo", "containerlab", "deploy", "-t", str(TOPO)])
    log("ContainerLab is up.", "PASS")


def clab_down():
    banner("ContainerLab — destroy")
    log("Tearing down topology...", "STEP")
    run(["sudo", "containerlab", "destroy", "-t", str(TOPO)], check=False)
    log("ContainerLab torn down.", "PASS")


def get_fabric_hosts() -> dict[str, str]:
    """Parse inventory.yml and return {hostname: ansible_host} for all FABRIC hosts."""
    with open(LAB_DIR / INVENTORY) as f:
        inv = yaml.safe_load(f)

    hosts = {}

    def walk(node):
        if isinstance(node, dict):
            if "hosts" in node:
                for name, vars_ in (node["hosts"] or {}).items():
                    ip = (vars_ or {}).get("ansible_host")
                    if ip:
                        hosts[name] = ip
            for key, val in node.items():
                if key != "hosts":
                    walk(val)

    fabric = inv.get("all", {}).get("children", {}).get("FABRIC", {})
    walk(fabric)
    return hosts


def get_eapi_credentials() -> tuple[str, str]:
    """Read pre-deploy eAPI credentials from group_vars/FABRIC/fabric.yml."""
    with open(FABRIC_VARS) as f:
        fabric = yaml.safe_load(f)
    user = fabric.get("eapi_user", "admin")
    password = fabric.get("eapi_password", "admin")
    return user, password


def get_deployed_credentials() -> tuple[str, str]:
    """Read post-deploy eAPI credentials (AVD ansible user) from group_vars/FABRIC/fabric.yml."""
    with open(FABRIC_VARS) as f:
        fabric = yaml.safe_load(f)
    user = fabric.get("ansible_user", "ansible")
    password = fabric.get("ansible_password", "ansible")
    return user, password


def get_git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT, check=True,
        ).stdout.strip()
    except Exception:
        return "unknown"


def wait_for_devices(timeout: int = 300, interval: int = 10):
    """Poll each cEOS device's eAPI until responsive or timeout is reached."""
    banner("STEP 1b: Waiting for devices to be ready")

    devices = get_fabric_hosts()
    if not devices:
        log("No devices found in inventory — skipping readiness check.", "WARN")
        return

    user, password = get_eapi_credentials()
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    pending  = set(devices.keys())
    deadline = time.time() + timeout
    log(f"Polling eAPI on {len(pending)} devices (timeout: {timeout}s, interval: {interval}s)...", "STEP")

    while pending and time.time() < deadline:
        for hostname in sorted(list(pending)):
            ip  = devices[hostname]
            url = f"https://{ip}/command-api"
            req = urllib.request.Request(
                url,
                data=b'{"jsonrpc":"2.0","method":"runCmds","params":{"version":1,"cmds":["show version"]},"id":1}',
                headers={"Content-Type": "application/json", "Authorization": f"Basic {token}"},
                method="POST",
            )
            try:
                urllib.request.urlopen(req, context=ssl_ctx, timeout=5)
                log(f"  {hostname} ({ip}) ready", "PASS")
                pending.remove(hostname)
            except Exception:
                pass

        if pending:
            remaining = int(deadline - time.time())
            log(f"  Waiting — {len(pending)} device(s) not ready yet ({remaining}s left)...", "INFO")
            time.sleep(interval)

    if pending:
        log(f"Timed out waiting for: {', '.join(sorted(pending))}", "FAIL")
        raise TimeoutError(f"Devices not ready after {timeout}s")

    log("All devices ready.", "PASS")


def avd_build():
    banner("STEP 2: AVD Build")
    log("Generating configs and documentation...", "STEP")
    run(["ansible-playbook", "-i", str(INVENTORY), str(BUILD_PLAY)], use_venv=True)
    log("Build complete.", "PASS")


def avd_deploy():
    banner("STEP 3: AVD Deploy")
    log("Deploying configurations to devices...", "STEP")
    run(["ansible-playbook", "-i", str(INVENTORY), str(DEPLOY_PLAY)], use_venv=True)
    log("Deploy complete.", "PASS")


def wait_for_convergence(timeout: int = 120, interval: int = 10):
    """Poll BGP summary on all FABRIC devices until all session message queues are empty."""
    if timeout <= 0:
        return
    banner("STEP 3b: Waiting for BGP/EVPN convergence")

    devices = get_fabric_hosts()
    if not devices:
        log("No devices found in inventory — skipping convergence check.", "WARN")
        return

    user, password = get_deployed_credentials()
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    payload = json.dumps({
        "jsonrpc": "2.0", "method": "runCmds",
        "params": {"version": 1, "cmds": ["show bgp summary"]}, "id": 1,
    }).encode()

    deadline = time.time() + timeout
    log(f"Polling BGP on {len(devices)} devices until sessions converge (timeout: {timeout}s)...", "STEP")

    while time.time() < deadline:
        busy = []
        for hostname, ip in sorted(devices.items()):
            req = urllib.request.Request(
                f"https://{ip}/command-api",
                data=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Basic {token}"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, context=ssl_ctx, timeout=5) as resp:
                    data = json.loads(resp.read())
                peers = data["result"][0].get("vrfs", {}).get("default", {}).get("peers", {})
                for peer, info in peers.items():
                    inq = info.get("inMsgQueue", 0)
                    outq = info.get("outMsgQueue", 0)
                    if inq > 0 or outq > 0:
                        busy.append(f"{hostname}→{peer} InQ={inq} OutQ={outq}")
            except Exception:
                pass  # device unreachable — skip

        if not busy:
            log("BGP sessions converged on all devices.", "PASS")
            wait_for_evpn_convergence()
            return

        remaining = int(deadline - time.time())
        for entry in busy:
            log(f"  {entry} ({remaining}s left)", "INFO")
        time.sleep(interval)

    log("BGP convergence timeout — proceeding anyway.", "WARN")


def wait_for_evpn_convergence(timeout: int = 120, interval: int = 5):
    """Wait until the EVPN overlay has fully settled before running ANTA.

    Queue-empty checks are racy — cEOS generates burst after burst of EVPN
    Type-2 advertisements as configs apply and the FIB is programmed.  A more
    reliable signal is *prefix-count stability*: when prefixReceived stops
    changing between polls the topology has actually converged.

    Two phases:
      Phase 1 — sessions Established, prefixReceived > 0, counts stable × 2.
      Phase 2 — 10 s FIB wait, then counts stable × 2 again (FIB programming
                 triggers a second wave of Type-2 advertisements).
    """
    devices = get_fabric_hosts()
    user, password = get_deployed_credentials()
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    payload = json.dumps({
        "jsonrpc": "2.0", "method": "runCmds",
        "params": {"version": 1, "cmds": ["show bgp evpn summary"]}, "id": 1,
    }).encode()

    def _snapshot() -> tuple[dict, list[str]]:
        """Return ({host: {peer: prefixReceived}}, [issue strings]).

        Issues are raised for: sessions not Established, prefixReceived == 0,
        or outMsgQueue > 0 (pending reflections not yet sent).
        Prefix-count stability catches new advertisements; queue checks catch
        in-flight reflections — both are required for true convergence.
        """
        counts, issues = {}, []
        for hostname, ip in sorted(devices.items()):
            req = urllib.request.Request(
                f"https://{ip}/command-api",
                data=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Basic {token}"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, context=ssl_ctx, timeout=5) as resp:
                    data = json.loads(resp.read())
                peers = data["result"][0].get("vrfs", {}).get("default", {}).get("peers", {})
                if not peers:
                    issues.append(f"{hostname}: no EVPN peers yet")
                    continue
                counts[hostname] = {}
                for peer, info in peers.items():
                    state    = info.get("peerState", "")
                    prefixes = info.get("prefixReceived", 0)
                    outq     = info.get("outMsgQueue", 0)
                    counts[hostname][peer] = prefixes
                    if state != "Established" or prefixes == 0:
                        issues.append(f"{hostname}→{peer} state={state} prefixes={prefixes}")
                    elif outq > 0:
                        issues.append(f"{hostname}→{peer} OutQ={outq} (reflecting)")
            except Exception:
                pass  # device unreachable — skip
        return counts, issues

    def _wait_stable(label: str, phase_timeout: int):
        """Require 2 consecutive polls where queues are empty AND prefix counts unchanged."""
        deadline = time.time() + phase_timeout
        prev, consecutive = None, 0
        log(f"{label} — polling {len(devices)} devices (timeout: {phase_timeout}s)...", "STEP")
        while time.time() < deadline:
            counts, issues = _snapshot()
            if not issues and counts == prev:
                consecutive += 1
                if consecutive >= 2:
                    log(f"{label} — stable (queues empty, prefix counts unchanged).", "PASS")
                    return
                log(f"{label} — clean ({consecutive}/2)...", "INFO")
            else:
                consecutive = 0
                remaining = int(deadline - time.time())
                for entry in issues:
                    log(f"  {entry} ({remaining}s left)", "INFO")
            prev = counts if not issues else None
            time.sleep(interval)
        log(f"{label} — timeout, proceeding anyway.", "WARN")

    # Phase 1: wait for EVPN prefix counts to stabilise
    _wait_stable("Phase 1: EVPN convergence", timeout)

    # Phase 2: FIB install triggers a second wave of Type-2 advertisements — wait again
    log("Waiting 10s for FIB programming...", "INFO")
    time.sleep(10)
    _wait_stable("Phase 2: post-FIB stability", 60)


BATFISH_CONTAINER = "batfish-pipeline"


def _batfish_reachable() -> bool:
    try:
        s = socket.create_connection(("localhost", 9996), timeout=2)
        s.close()
        return True
    except OSError:
        return False


def start_batfish() -> bool:
    """Start the Batfish container if not already running. Returns True if we started it."""
    banner("Batfish — Starting container")
    if _batfish_reachable():
        log("Batfish already running at localhost:9996 — reusing.", "INFO")
        return False

    log("Starting Batfish container (batfish/allinone)...", "STEP")
    result = subprocess.run(
        ["docker", "run", "-d", "--name", BATFISH_CONTAINER,
         "-p", "9996:9996", "batfish/allinone"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to start Batfish container: {result.stderr.strip()}\n"
            "Is Docker running? Try: docker info"
        )

    log("Waiting for Batfish to be ready...", "INFO")
    deadline = time.time() + 60
    while time.time() < deadline:
        if _batfish_reachable():
            log("Batfish container ready.", "PASS")
            return True
        time.sleep(3)

    raise RuntimeError("Batfish container started but not reachable after 60s.")


def stop_batfish():
    """Stop and remove the Batfish container started by this pipeline run."""
    banner("Batfish — Stopping container")
    subprocess.run(["docker", "stop", BATFISH_CONTAINER], capture_output=True)
    subprocess.run(["docker", "rm",   BATFISH_CONTAINER], capture_output=True)
    log("Batfish container stopped.", "PASS")


def batfish_analyze():
    banner("STEP 2b: Batfish — Static Config Analysis")

    try:
        import logging
        from pybatfish.client.session import Session
    except ImportError:
        raise RuntimeError("pybatfish is not installed. Run: pip install pybatfish")

    logging.getLogger("pybatfish").setLevel(logging.ERROR)

    if not CONFIGS_DIR.exists() or not any(CONFIGS_DIR.glob("*.cfg")):
        raise RuntimeError(f"No .cfg files found in {CONFIGS_DIR}. Run 'make build' first.")

    cfgs = list(CONFIGS_DIR.glob("*.cfg"))
    log(f"Batfish reachable. Staging {len(cfgs)} config(s) for snapshot upload...", "INFO")

    # Batfish snapshot root must contain a configs/ subdirectory
    with tempfile.TemporaryDirectory(prefix="batfish-snap-") as snap_root:
        snap_configs = Path(snap_root) / "configs"
        snap_configs.mkdir()
        for cfg in cfgs:
            shutil.copy2(cfg, snap_configs / cfg.name)

        bf = Session(host="localhost")
        bf.set_network("avd-lab")
        bf.init_snapshot(snap_root, name="snapshot", overwrite=True)

    log(f"Snapshot loaded from: {CONFIGS_DIR}", "INFO")

    # Run all three queries upfront so DataFrames are available for both analysis and CSV export
    log("Querying Batfish (initIssues, bgpSessionCompatibility, undefinedReferences)...", "STEP")
    df_init  = bf.q.initIssues().answer().frame()
    df_bgp   = bf.q.bgpSessionCompatibility().answer().frame()
    df_undef = bf.q.undefinedReferences().answer().frame()

    issues_found    = []
    init_warnings   = 0
    init_errors     = 0
    bgp_ok          = 0
    bgp_warnings    = 0
    bgp_failures    = 0
    undef_fp        = 0
    undef_blocking  = 0

    # --- initIssues ---
    # Columns: Nodes, Source_Lines, Type, Details, Line_Text, Parser_Context
    # Both "Parse warning" and "Parse error" are Batfish EOS parser limitations for cEOS AVD
    # configs (unrecognised EOS syntax, NPEs on valid EOS address-family commands, etc.).
    # Treat all as informational WARNs — non-BGP undefinedReferences catch real missing defs.
    log("initIssues...", "STEP")
    if df_init.empty:
        log("initIssues: no issues.", "PASS")
    else:
        errors   = df_init[df_init["Type"] == "Parse error"]
        warnings = df_init[df_init["Type"] != "Parse error"]
        init_warnings = len(warnings)
        init_errors   = len(errors)
        if not warnings.empty:
            log(f"initIssues: {init_warnings} parse warning(s) — unrecognised EOS syntax (expected for cEOS).", "WARN")
        if not errors.empty:
            log(f"initIssues: {init_errors} parse error(s) — Batfish EOS parser limitation(s) (expected for cEOS).", "WARN")
        if warnings.empty and errors.empty:
            log("initIssues: no issues.", "PASS")

    # --- bgpSessionCompatibility ---
    # Columns: Node, VRF, Local_AS, Local_Interface, Local_IP, Remote_AS, Remote_Node,
    #          Remote_Interface, Remote_IP, Address_Families, Session_Type, Configured_Status
    # UNIQUE_MATCH  → OK
    # NO_LOCAL_IP / UNKNOWN_REMOTE / HALF_OPEN → known cEOS/MLAG Batfish limitations → WARN
    # anything else → blocking
    log("bgpSessionCompatibility...", "STEP")
    if df_bgp.empty:
        log("bgpSessionCompatibility: no sessions found (check snapshot).", "WARN")
    else:
        for _, row in df_bgp.iterrows():
            status = str(row.get("Configured_Status", "")).upper()
            if status == "UNIQUE_MATCH":
                bgp_ok += 1
                continue
            msg = (
                f"{row.get('Node','?')}[{row.get('VRF','default')}] "
                f"{row.get('Local_IP','?')} -> {row.get('Remote_Node','?')} "
                f"{row.get('Remote_IP','?')} ({row.get('Session_Type','?')}): {status}"
            )
            if status in ("HALF_OPEN", "NO_LOCAL_IP", "UNKNOWN_REMOTE"):
                bgp_warnings += 1
            else:
                bgp_failures += 1
                log(msg, "FAIL")
                issues_found.append(msg)
        if bgp_warnings:
            log(f"bgpSessionCompatibility: {bgp_warnings} session(s) with expected cEOS/MLAG limitations (NO_LOCAL_IP/UNKNOWN_REMOTE/HALF_OPEN).", "WARN")
        log(f"bgpSessionCompatibility: {bgp_ok} UNIQUE_MATCH session(s).",
            "PASS" if bgp_ok > 0 else "WARN")

    # --- undefinedReferences ---
    # Columns: File_Name, Struct_Type, Ref_Name, Context, Lines
    # BGP peer-group types are Batfish parser false positives for EOS → WARN
    # Other types (route-map, prefix-list, etc.) indicate real missing definitions → blocking
    log("undefinedReferences...", "STEP")
    if df_undef.empty:
        log("undefinedReferences: none found.", "PASS")
    else:
        for _, row in df_undef.iterrows():
            struct_type = str(row.get("Struct_Type", "")).lower()
            msg = (
                f"Undefined in {row.get('File_Name','?')}: "
                f"{row.get('Struct_Type','')} '{row.get('Ref_Name','')}' "
                f"({row.get('Context','')})"
            )
            if "bgp" in struct_type:
                undef_fp += 1
            else:
                undef_blocking += 1
                log(msg, "FAIL")
                issues_found.append(msg)
        if undef_fp:
            log(f"undefinedReferences: {undef_fp} BGP peer-group reference(s) — known cEOS false positive(s).", "WARN")
        if not issues_found:
            log("undefinedReferences: no non-BGP undefined references found.", "PASS")

    # --- Write CSVs ---
    BATFISH_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_init.to_csv( BATFISH_REPORT_DIR / "init_issues.csv",    index=False)
    df_bgp.to_csv(  BATFISH_REPORT_DIR / "bgp_sessions.csv",   index=False)
    df_undef.to_csv(BATFISH_REPORT_DIR / "undefined_refs.csv", index=False)
    log(f"Batfish CSVs written to {BATFISH_REPORT_DIR}/", "INFO")

    summary = {
        "init_warnings":  init_warnings,
        "init_errors":    init_errors,
        "bgp_ok":         bgp_ok,
        "bgp_warnings":   bgp_warnings,
        "bgp_failures":   bgp_failures,
        "undef_fp":       undef_fp,
        "undef_blocking": undef_blocking,
        "blocking_issues": len(issues_found),
    }

    if issues_found:
        log(f"Batfish found {len(issues_found)} blocking issue(s).", "FAIL")
    else:
        log("Batfish static analysis PASSED — configs look clean.", "PASS")

    return summary


def avd_validate():
    banner("STEP 4: AVD Validate (ANTA)")
    log("Running validation tests...", "STEP")
    run(["ansible-playbook", "-i", str(INVENTORY), str(VALIDATE_PLAY)], use_venv=True)
    log("Validation playbook complete.", "PASS")


# ---------------------------------------------------------------------------
# Results parsing
# ---------------------------------------------------------------------------

def parse_results() -> tuple[int, int, int, list[dict]]:
    """Read anta_report.csv → (passed, failed, skipped, failure_rows)."""
    if not RESULTS_CSV.exists():
        log(f"Results file not found: {RESULTS_CSV}", "WARN")
        return 0, 0, 0, []

    passed = failed = skipped = 0
    failures = []
    with open(RESULTS_CSV, newline="") as f:
        for row in csv.DictReader(f):
            result = row["Test Status"].strip().lower()
            if result == "success":
                passed += 1
            elif result in ("failure", "error"):
                failed += 1
                failures.append(row)
            elif result == "skipped":
                skipped += 1
    return passed, failed, skipped, failures


def print_report(passed: int, failed: int, skipped: int, failures: list[dict]):
    banner("VALIDATION REPORT")
    total = passed + failed + skipped
    log(f"Total:   {total}")
    log(f"Passed:  {passed}", "PASS" if passed else "INFO")
    log(f"Skipped: {skipped}")
    if failed:
        log(f"Failed:  {failed}", "FAIL")
        print()
        log("Failed tests:", "FAIL")
        for row in failures:
            device  = row["Device"]
            test    = row["Test Name"]
            message = row["Message(s)"]
            log(f"  [{device}] {test} — {message}", "FAIL")
    else:
        log(f"Failed:  {failed}", "PASS")


# ---------------------------------------------------------------------------
# Pipeline report artifact
# ---------------------------------------------------------------------------

def _fmt_duration(seconds: int) -> str:
    mins, secs = divmod(seconds, 60)
    return f"{mins}m {secs}s" if mins else f"{secs}s"


def _build_md(report: dict, history: list) -> str:
    """Return a GFM Markdown report: run history + full detail of the latest run."""
    ICONS = {"PASS": "OK", "FAIL": "FAIL", "SKIP": "--", "NOT_RUN": "  "}

    ts       = report.get("timestamp", "").replace("T", " ")
    result   = report.get("result", "UNKNOWN")
    duration = _fmt_duration(report.get("duration_s", 0))
    commit   = report.get("git_commit", "unknown")
    steps    = report.get("steps", {})
    batfish  = report.get("batfish")
    anta     = report.get("anta")

    lines = []

    # --- Header ---
    lines.append(f"# AVD Pipeline Report — {result}")
    lines.append("")
    lines.append(f"**{ts}** | Duration: {duration} | Commit: `{commit}`")
    lines.append("")

    # --- Run history table ---
    step_names = list(steps.keys())
    header_cells = " | ".join(s.replace("_", " ").title() for s in step_names)
    lines.append(f"## Run History (last {len(history)})")
    lines.append("")
    lines.append(f"| Timestamp | Result | Commit | Duration | {header_cells} | BF Issues | ANTA |")
    lines.append(f"|-----------|--------|--------|----------|{'|'.join('---' for _ in step_names)}|-----------|------|")

    for entry in reversed(history):  # newest first
        e_ts     = entry.get("timestamp", "").replace("T", " ")
        e_res    = entry.get("result", "?")
        e_dur    = _fmt_duration(entry.get("duration_s", 0))
        e_commit = entry.get("git_commit", "?")
        e_steps  = entry.get("steps", {})
        e_bf     = entry.get("batfish_blocking")
        e_anta_p = entry.get("anta_passed")
        e_anta_f = entry.get("anta_failed")

        step_cells = " | ".join(ICONS.get(e_steps.get(s, "NOT_RUN"), "?") for s in step_names)
        bf_cell    = "—" if e_bf is None else str(e_bf)
        anta_cell  = "—" if e_anta_p is None else (
            f"{e_anta_p} pass" + (f" / **{e_anta_f} fail**" if e_anta_f else "")
        )
        lines.append(
            f"| {e_ts} | **{e_res}** | `{e_commit}` | {e_dur} | {step_cells} | {bf_cell} | {anta_cell} |"
        )

    lines.append("")

    # --- This run step detail ---
    lines.append("## This Run — Steps")
    lines.append("")
    lines.append("| Step | Status |")
    lines.append("|------|--------|")
    for step, status in steps.items():
        icon = ICONS.get(status, status)
        lines.append(f"| {step.replace('_', ' ').title()} | {icon} |")
    lines.append("")

    # --- Batfish section ---
    if batfish is not None:
        bf = batfish
        blocking = bf.get("blocking_issues", 0)
        verdict  = "PASSED — no blocking issues" if not blocking else f"FAILED — {blocking} blocking issue(s)"
        lines.append("## Batfish Static Analysis")
        lines.append("")
        lines.append(f"**{verdict}**")
        lines.append("")
        lines.append("| Check | Count |")
        lines.append("|-------|-------|")
        lines.append(f"| Init warnings (unrecognised EOS syntax) | {bf.get('init_warnings', 0)} |")
        lines.append(f"| Init errors (Batfish parser gaps)        | {bf.get('init_errors', 0)} |")
        lines.append(f"| BGP sessions matched (UNIQUE_MATCH)      | {bf.get('bgp_ok', 0)} |")
        lines.append(f"| BGP warnings (cEOS peer-group limits)    | {bf.get('bgp_warnings', 0)} |")
        lines.append(f"| BGP failures (blocking)                  | {bf.get('bgp_failures', 0)} |")
        lines.append(f"| Undefined refs — BGP (false positives)   | {bf.get('undef_fp', 0)} |")
        lines.append(f"| Undefined refs — non-BGP (blocking)      | {bf.get('undef_blocking', 0)} |")
        lines.append(f"| **Total blocking issues**                | **{blocking}** |")
        lines.append("")

    # --- ANTA section ---
    if anta is not None:
        lines.append("## ANTA Validation")
        lines.append("")
        lines.append("| Result | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Total   | {anta.get('total', 0)} |")
        lines.append(f"| Passed  | {anta.get('passed', 0)} |")
        lines.append(f"| Skipped | {anta.get('skipped', 0)} |")
        lines.append(f"| Failed  | {anta.get('failed', 0)} |")
        lines.append("")

        failures = anta.get("failures", [])
        if failures:
            lines.append("### Failed Tests")
            lines.append("")
            lines.append("| Device | Test | Message |")
            lines.append("|--------|------|---------|")
            for row in failures:
                device  = str(row.get("Device", "")).replace("|", "\\|")
                test    = str(row.get("Test Name", "")).replace("|", "\\|")
                message = str(row.get("Message(s)", "")).replace("|", "\\|")
                lines.append(f"| {device} | {test} | {message} |")
            lines.append("")

    return "\n".join(lines)


def write_pipeline_report(report: dict):
    """Append compact summary to history.json (keep 10) and write latest.html."""
    PIPELINE_RUNS_DIR.mkdir(parents=True, exist_ok=True)

    # Build compact summary for history
    anta    = report.get("anta") or {}
    batfish = report.get("batfish") or {}
    summary = {
        "timestamp":        report["timestamp"],
        "result":           report["result"],
        "duration_s":       report["duration_s"],
        "git_commit":       report.get("git_commit", "unknown"),
        "steps":            report["steps"],
        "batfish_blocking": batfish.get("blocking_issues") if report.get("batfish") is not None else None,
        "anta_passed":      anta.get("passed")  if report.get("anta") is not None else None,
        "anta_failed":      anta.get("failed")  if report.get("anta") is not None else None,
        "anta_skipped":     anta.get("skipped") if report.get("anta") is not None else None,
    }

    # Load existing history, append, keep last 10
    history = []
    if HISTORY_JSON.exists():
        try:
            history = json.loads(HISTORY_JSON.read_text())
        except Exception:
            history = []
    history.append(summary)
    history = history[-10:]

    HISTORY_JSON.write_text(json.dumps(history, indent=2, default=str))
    LATEST_MD.write_text(_build_md(report, history))
    log(f"Pipeline report updated: {PIPELINE_RUNS_DIR}/", "INFO")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the AVD ContainerLab pipeline: up → build → deploy → validate → down"
    )
    parser.add_argument(
        "--skip-clab-up", action="store_true",
        help="Skip ContainerLab deploy (assume lab is already running)",
    )
    parser.add_argument(
        "--skip-build", action="store_true",
        help="Skip AVD build step",
    )
    parser.add_argument(
        "--skip-deploy", action="store_true",
        help="Skip AVD deploy step",
    )
    parser.add_argument(
        "--convergence-wait",
        type=int,
        default=120,
        metavar="SECONDS",
        help="Max seconds to poll BGP convergence after deploy (default: 120, 0 to skip)",
    )
    parser.add_argument(
        "--teardown",
        choices=["always", "on-pass", "never"],
        default="on-pass",
        metavar="{always,on-pass,never}",
        help="When to tear down the lab (default: on-pass)",
    )
    parser.add_argument(
        "--skip-batfish", action="store_true",
        help="Skip Batfish static config analysis",
    )
    parser.add_argument(
        "--skip-validate", action="store_true",
        help="Skip ANTA validation and result parsing (use with --batfish for lab-free checks)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    lab_is_up       = False
    batfish_started = False
    pipeline_ok     = True
    run_ts          = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    start_time      = time.time()
    current_step    = None
    batfish_summary = None
    anta_result     = None

    steps = {
        "clab_up":  "SKIP" if args.skip_clab_up  else "NOT_RUN",
        "build":    "SKIP" if args.skip_build     else "NOT_RUN",
        "batfish":  "SKIP" if args.skip_batfish   else "NOT_RUN",
        "deploy":   "SKIP" if args.skip_deploy    else "NOT_RUN",
        "validate": "SKIP" if args.skip_validate  else "NOT_RUN",
    }

    def handle_signal(sig, frame):
        print()
        log("Interrupted — attempting lab cleanup...", "WARN")
        if lab_is_up:
            clab_down()
        sys.exit(1)

    signal.signal(signal.SIGINT,  handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    banner(f"AVD Digital Twin Pipeline  [{run_ts.replace('T', ' ')}]")

    # --- Argument warnings ---
    if args.skip_clab_up and not args.skip_deploy:
        log("--skip-clab-up set: assuming lab is already running — deploy will fail if devices are not reachable.", "WARN")
    if args.skip_build and not args.skip_batfish:
        log("--skip-build set: Batfish will analyse existing configs in intended/configs — may be stale.", "WARN")
    if args.skip_build and not args.skip_deploy:
        log("--skip-build set: deploying existing configs in intended/configs — may be stale.", "WARN")

    try:
        if not args.skip_clab_up:
            current_step = "clab_up"
            clab_up()
            wait_for_devices()
            steps["clab_up"] = "PASS"
        else:
            log("Skipping clab-up (--skip-clab-up)", "WARN")
            if not args.skip_deploy:
                wait_for_devices()
        lab_is_up = True

        if not args.skip_build:
            current_step = "build"
            avd_build()
            steps["build"] = "PASS"

        if not args.skip_batfish:
            batfish_started = start_batfish()
            current_step = "batfish"
            batfish_summary = batfish_analyze()
            if batfish_summary.get("blocking_issues", 0) > 0:
                steps["batfish"] = "FAIL"
                raise RuntimeError(
                    f"Batfish static analysis FAILED with "
                    f"{batfish_summary['blocking_issues']} blocking issue(s)."
                )
            steps["batfish"] = "PASS"

        if not args.skip_deploy:
            current_step = "deploy"
            avd_deploy()
            wait_for_convergence(args.convergence_wait)
            steps["deploy"] = "PASS"

        if not args.skip_validate:
            current_step = "validate"
            avd_validate()

            passed, failed, skipped, failures = parse_results()
            print_report(passed, failed, skipped, failures)

            anta_result = {
                "total":    passed + failed + skipped,
                "passed":   passed,
                "skipped":  skipped,
                "failed":   failed,
                "failures": failures,
            }

            if failed:
                pipeline_ok = False
                steps["validate"] = "FAIL"
            else:
                steps["validate"] = "PASS"

    except subprocess.CalledProcessError as e:
        log(f"Step failed (exit {e.returncode})", "FAIL")
        pipeline_ok = False
        if current_step and steps.get(current_step) not in ("PASS", "SKIP"):
            steps[current_step] = "FAIL"
    except (TimeoutError, RuntimeError) as e:
        log(str(e), "FAIL")
        pipeline_ok = False
        if current_step and steps.get(current_step) not in ("PASS", "SKIP", "FAIL"):
            steps[current_step] = "FAIL"

    finally:
        if batfish_started:
            stop_batfish()
        should_teardown = (
            args.teardown == "always"
            or (args.teardown == "on-pass" and pipeline_ok)
        )
        if lab_is_up and should_teardown:
            clab_down()
        elif lab_is_up:
            log("Lab left running — use 'make clab-down' to destroy.", "WARN")

        report = {
            "timestamp":  run_ts,
            "result":     "PASSED" if pipeline_ok else "FAILED",
            "duration_s": int(time.time() - start_time),
            "git_commit": get_git_commit(),
            "steps":      steps,
            "batfish":    batfish_summary,
            "anta":       anta_result,
        }
        try:
            write_pipeline_report(report)
        except Exception as exc:
            log(f"Could not write pipeline report: {exc}", "WARN")

    if pipeline_ok:
        banner("PIPELINE PASSED")
        sys.exit(0)
    else:
        banner("PIPELINE FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
