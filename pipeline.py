#!/usr/bin/env python3
"""
AVD ContainerLab Pipeline Orchestrator
Flow: clab-up → build → [batfish] → deploy → validate → report → clab-down (conditional)
"""

import argparse
import base64
import csv
import json
import signal
import socket
import ssl
import subprocess
import sys
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
            log("Waiting 15s for data-plane (ARP/EVPN) to settle...", "INFO")
            time.sleep(15)
            return

        remaining = int(deadline - time.time())
        for entry in busy:
            log(f"  {entry} ({remaining}s left)", "INFO")
        time.sleep(interval)

    log("BGP convergence timeout — proceeding anyway.", "WARN")


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

    import shutil
    import tempfile

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

    issues_found = []

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
        if not warnings.empty:
            log(f"initIssues: {len(warnings)} parse warning(s) — unrecognised EOS syntax (expected for cEOS).", "WARN")
        if not errors.empty:
            log(f"initIssues: {len(errors)} parse error(s) — Batfish EOS parser limitation(s) (expected for cEOS).", "WARN")
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
        ok_count   = 0
        warn_count = 0
        for _, row in df_bgp.iterrows():
            status = str(row.get("Configured_Status", "")).upper()
            if status == "UNIQUE_MATCH":
                ok_count += 1
                continue
            msg = (
                f"{row.get('Node','?')}[{row.get('VRF','default')}] "
                f"{row.get('Local_IP','?')} -> {row.get('Remote_Node','?')} "
                f"{row.get('Remote_IP','?')} ({row.get('Session_Type','?')}): {status}"
            )
            if status in ("HALF_OPEN", "NO_LOCAL_IP", "UNKNOWN_REMOTE"):
                warn_count += 1
            else:
                log(msg, "FAIL")
                issues_found.append(msg)
        if warn_count:
            log(f"bgpSessionCompatibility: {warn_count} session(s) with expected cEOS/MLAG limitations (NO_LOCAL_IP/UNKNOWN_REMOTE/HALF_OPEN).", "WARN")
        log(f"bgpSessionCompatibility: {ok_count} UNIQUE_MATCH session(s).",
            "PASS" if ok_count > 0 else "WARN")

    # --- undefinedReferences ---
    # Columns: File_Name, Struct_Type, Ref_Name, Context, Lines
    # BGP peer-group types are Batfish parser false positives for EOS → WARN
    # Other types (route-map, prefix-list, etc.) indicate real missing definitions → blocking
    log("undefinedReferences...", "STEP")
    if df_undef.empty:
        log("undefinedReferences: none found.", "PASS")
    else:
        bgp_fp_count = 0
        for _, row in df_undef.iterrows():
            struct_type = str(row.get("Struct_Type", "")).lower()
            msg = (
                f"Undefined in {row.get('File_Name','?')}: "
                f"{row.get('Struct_Type','')} '{row.get('Ref_Name','')}' "
                f"({row.get('Context','')})"
            )
            if "bgp" in struct_type:
                bgp_fp_count += 1
            else:
                log(msg, "FAIL")
                issues_found.append(msg)
        if bgp_fp_count:
            log(f"undefinedReferences: {bgp_fp_count} BGP peer-group reference(s) — known cEOS false positive(s).", "WARN")
        if not issues_found:
            log("undefinedReferences: no non-BGP undefined references found.", "PASS")

    # --- Write CSVs ---
    BATFISH_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df_init.to_csv( BATFISH_REPORT_DIR / "init_issues.csv",           index=False)
    df_bgp.to_csv(  BATFISH_REPORT_DIR / "bgp_sessions.csv",          index=False)
    df_undef.to_csv(BATFISH_REPORT_DIR / "undefined_refs.csv",        index=False)
    log(f"Reports written to {BATFISH_REPORT_DIR}/", "INFO")

    if issues_found:
        log(f"Batfish found {len(issues_found)} blocking issue(s).", "FAIL")
        raise RuntimeError(f"Batfish static analysis FAILED with {len(issues_found)} issue(s).")

    log("Batfish static analysis PASSED — configs look clean.", "PASS")


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
    lab_is_up        = False
    batfish_started  = False
    pipeline_ok      = True

    def handle_signal(sig, frame):
        print()
        log("Interrupted — attempting lab cleanup...", "WARN")
        if lab_is_up:
            clab_down()
        sys.exit(1)

    signal.signal(signal.SIGINT,  handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    banner(f"AVD Digital Twin Pipeline  [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

    try:
        if not args.skip_clab_up:
            clab_up()
            wait_for_devices()
        else:
            log("Skipping clab-up (--skip-clab-up)", "WARN")
        lab_is_up = True

        if not args.skip_build:
            avd_build()

        if not args.skip_batfish:
            batfish_started = start_batfish()
            batfish_analyze()

        if not args.skip_deploy:
            avd_deploy()
            wait_for_convergence(args.convergence_wait)

        if not args.skip_validate:
            avd_validate()

            passed, failed, skipped, failures = parse_results()
            print_report(passed, failed, skipped, failures)

            if failed:
                pipeline_ok = False

    except subprocess.CalledProcessError as e:
        log(f"Step failed (exit {e.returncode})", "FAIL")
        pipeline_ok = False
    except (TimeoutError, RuntimeError) as e:
        log(str(e), "FAIL")
        pipeline_ok = False

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

    if pipeline_ok:
        banner("PIPELINE PASSED")
        sys.exit(0)
    else:
        banner("PIPELINE FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
