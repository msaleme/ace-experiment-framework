#!/usr/bin/env python3
"""Compatibility wrapper for phase-2 execution.

This script now delegates to the full closed-loop program and keeps only
near-term experiments, preserving the original command entrypoint.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="ACE Experiment Framework - Phase 2 Runner")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Workspace root")
    args = parser.parse_args()

    from run_full_program import run_full_program

    rc = run_full_program(args.workspace)
    if rc != 0:
        return rc

    # Keep a phase-2 only summary for quick checks.
    summary_path = args.workspace / "reports" / "full_program_summary.json"
    phase2_path = args.workspace / "reports" / "phase2_summary.json"
    if summary_path.exists():
        data = json.loads(summary_path.read_text(encoding="utf-8"))
        data["lane"] = "near_term"
        phase2_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
