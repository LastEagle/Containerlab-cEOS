#!/usr/bin/env python3
"""
AVD ContainerLab Pipeline Orchestrator
Flow: clab-up → build → deploy → validate → report → clab-down (conditional)
"""

import argparse
import csv
import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT     = Path(__file__).parent
LAB_DIR       = REPO_ROOT / "arista-avd-lab"
TOPO          = LAB_DIR / "clab-topo.yml"
VENV_ACTIVATE = LAB_DIR / "cenv" / "bin" / "activate"
RESULTS_CSV   = LAB_DIR / "reports" / "FABRIC-state.csv"

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


def avd_validate():
    banner("STEP 4: AVD Validate (ANTA)")
    log("Running validation tests...", "STEP")
    run(["ansible-playbook", "-i", str(INVENTORY), str(VALIDATE_PLAY)], use_venv=True)
    log("Validation playbook complete.", "PASS")


# ---------------------------------------------------------------------------
# Results parsing
# ---------------------------------------------------------------------------

def parse_results() -> tuple[int, int, int, list[dict]]:
    """Read FABRIC-state.csv → (passed, failed, skipped, failure_rows)."""
    if not RESULTS_CSV.exists():
        log(f"Results file not found: {RESULTS_CSV}", "WARN")
        return 0, 0, 0, []

    passed = failed = skipped = 0
    failures = []
    with open(RESULTS_CSV, newline="") as f:
        for row in csv.DictReader(f):
            result = row["result"].strip().upper()
            if result == "PASS":
                passed += 1
            elif result == "FAIL":
                failed += 1
                failures.append(row)
            elif result == "SKIPPED":
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
            device  = row["dut"]
            test    = row["test"]
            inputs  = row["inputs"]
            message = row["messages"]
            log(f"  [{device}] {test} — {inputs or message}", "FAIL")
            if inputs and message:
                log(f"           {message}", "FAIL")
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
        "--teardown",
        choices=["always", "on-pass", "never"],
        default="on-pass",
        metavar="{always,on-pass,never}",
        help="When to tear down the lab (default: on-pass)",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    lab_is_up    = False
    pipeline_ok  = True

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
        else:
            log("Skipping clab-up (--skip-clab-up)", "WARN")
        lab_is_up = True

        if not args.skip_build:
            avd_build()

        if not args.skip_deploy:
            avd_deploy()

        avd_validate()

        passed, failed, skipped, failures = parse_results()
        print_report(passed, failed, skipped, failures)

        if failed:
            pipeline_ok = False

    except subprocess.CalledProcessError as e:
        log(f"Step failed (exit {e.returncode})", "FAIL")
        pipeline_ok = False

    finally:
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
