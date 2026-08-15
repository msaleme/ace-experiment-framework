"""Stable command-line interface for ACE experiment contracts and run artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

from ace_lab import __version__
from ace_lab.evidence import EvidenceValidationError, assess_evidence, load_trial_evidence


REQUIRED_KEYS = (
    "baseline",
    "mutation_scope",
    "trials",
    "quality_floor",
    "benchmark_sets",
    "acceptance",
    "reporting",
)
REQUIRED_SPLITS = ("development", "validation", "holdout")
SAFE_EXPERIMENT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ConfigValidationError(ValueError):
    """Raised when an ACE experiment contract is incomplete or malformed."""


def load_and_validate_config(path: Path) -> dict[str, Any]:
    """Load an ACE YAML contract and enforce the stable public schema subset."""
    if not path.is_file():
        raise ConfigValidationError(f"config does not exist: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except yaml.YAMLError as exc:
        raise ConfigValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigValidationError("config must contain a mapping at its top level")

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ConfigValidationError(f"missing required keys: {', '.join(missing)}")
    if not isinstance(data["mutation_scope"], list) or not data["mutation_scope"]:
        raise ConfigValidationError("mutation_scope must be a non-empty list")
    if (
        isinstance(data["trials"], bool)
        or not isinstance(data["trials"], int)
        or data["trials"] < 1
    ):
        raise ConfigValidationError("trials must be a positive integer")
    if not isinstance(data["quality_floor"], dict):
        raise ConfigValidationError("quality_floor must be a mapping")
    if not isinstance(data["acceptance"], dict) or not isinstance(data["reporting"], dict):
        raise ConfigValidationError("acceptance and reporting must be mappings")
    sets = data["benchmark_sets"]
    if not isinstance(sets, dict):
        raise ConfigValidationError("benchmark_sets must be a mapping")
    absent = [split for split in REQUIRED_SPLITS if not sets.get(split)]
    if absent:
        raise ConfigValidationError(f"benchmark_sets must include non-empty: {', '.join(absent)}")
    experiment_id = data.get("experiment_id", path.stem)
    if not isinstance(experiment_id, str) or not SAFE_EXPERIMENT_ID.fullmatch(experiment_id):
        raise ConfigValidationError(
            "experiment_id must use only letters, numbers, dot, underscore, or hyphen"
        )
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dependency_versions() -> dict[str, str | None]:
    versions: dict[str, str | None] = {"python": platform.python_version()}
    for dependency in ("PyYAML", "numpy", "scipy"):
        try:
            versions[dependency] = importlib.metadata.version(dependency)
        except importlib.metadata.PackageNotFoundError:
            versions[dependency] = None
    return versions


def _source_revision() -> str | None:
    """Use an explicit build value first; Git is available only in a checkout."""
    revision = os.environ.get("ACE_SOURCE_REVISION")
    if revision:
        return revision
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _atomic_write(path: Path, content: str) -> None:
    """Persist a complete artifact or leave no partially written target behind."""
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)


def build_preflight(config_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    """Translate a valid contract into the next concrete work a researcher must do."""
    trial_config = config.get("trial_configuration", {})
    seeds = trial_config.get("seeds", [])
    split_counts = {split: len(config["benchmark_sets"][split]) for split in REQUIRED_SPLITS}
    warnings = []
    if not seeds:
        warnings.append("No explicit seeds declared. Record the seeds used before comparing runs.")
    elif len(seeds) != config["trials"]:
        warnings.append(
            f"Declared trials ({config['trials']}) and explicit seeds ({len(seeds)}) differ. "
            "Resolve the difference before execution."
        )
    if config.get("telemetry_provenance", "not-declared") == "not-declared":
        warnings.append(
            "Telemetry provenance is not declared. State whether power and runtime data are measured, estimated, or simulated."
        )
    return {
        "schema_version": "1.0",
        "artifact_type": "ace-preflight",
        "experiment_id": config.get("experiment_id", config_path.stem),
        "ready_to_measure": not warnings,
        "baseline": config["baseline"],
        "split_counts": split_counts,
        "declared_trials": config["trials"],
        "declared_seeds": seeds,
        "warnings": warnings,
        "next_actions": [
            "Pin the source revision and execution environment before the first trial.",
            "Run the declared trials for development, validation, and holdout splits without tuning on holdout.",
            "Retain raw metrics, telemetry source, and failed trials alongside the config digest.",
            "Apply the declared acceptance rules only after all split results are available.",
            "State the operating envelope and evidence boundary with any result; do not promote a contract record as a measured outcome.",
        ],
        "decision_help": (
            "ACE helps reviewers identify whether a result is ready to measure, ready to review, "
            "or still missing evidence before someone makes a deployment decision."
        ),
    }


def build_manifest(config_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    """Create a provenance record without asserting that a workload was measured."""
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    trial_config = config.get("trial_configuration", {})
    return {
        "schema_version": "1.0",
        "artifact_type": "ace-run-manifest",
        "created_at_utc": now,
        "package_version": __version__,
        "source_revision": _source_revision(),
        "python_version": platform.python_version(),
        "dependency_versions": _dependency_versions(),
        "config_path": str(config_path.resolve()),
        "config_sha256": _sha256(config_path),
        "experiment_id": config.get("experiment_id", config_path.stem),
        "seeds": trial_config.get("seeds", []),
        "baseline": config["baseline"],
        "benchmark_sets": config["benchmark_sets"],
        "telemetry_provenance": config.get("telemetry_provenance", "not-declared"),
        "preflight": build_preflight(config_path, config),
        "execution_mode": "contract-recording-only",
        "verdict": "inconclusive",
        "claim_boundary": (
            "This artifact records a validated experiment contract. It contains no measured "
            "performance result and must not be used as evidence of an optimization outcome."
        ),
    }


def write_run_artifacts(
    config_path: Path, output_dir: Path, *, force: bool = False
) -> tuple[Path, Path]:
    """Validate an experiment contract and persist a manifest plus human-readable report."""
    config = load_and_validate_config(config_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(config_path, config)
    stem = manifest["experiment_id"]
    manifest_path = output_dir / f"{stem}.manifest.json"
    report_path = output_dir / f"{stem}.report.md"
    existing = [str(path) for path in (manifest_path, report_path) if path.exists()]
    if existing and not force:
        raise ConfigValidationError(
            "refusing to overwrite run artifacts; pass --force: " + ", ".join(existing)
        )
    _atomic_write(manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    _atomic_write(
        report_path,
        "\n".join(
            [
                f"# ACE Run Record: {stem}",
                "",
                "## Status",
                "",
                "- Verdict: **INCONCLUSIVE**",
                "- Execution mode: contract-recording-only",
                "- No workload metrics were generated by this command.",
                "",
                "## Provenance",
                "",
                f"- Config SHA-256: `{manifest['config_sha256']}`",
                f"- Package version: `{manifest['package_version']}`",
                f"- Created: `{manifest['created_at_utc']}`",
                f"- Manifest: `{manifest_path.name}`",
                "",
                "## Claim boundary",
                "",
                manifest["claim_boundary"],
                "",
                "## What to do next",
                "",
                *[f"- {action}" for action in manifest["preflight"]["next_actions"]],
                "",
                "## Preflight warnings",
                "",
                *([f"- {warning}" for warning in manifest["preflight"]["warnings"]] or ["- None"]),
                "",
            ]
        ),
    )
    return manifest_path, report_path


def write_assessment_artifacts(
    config_path: Path, results_path: Path, output_dir: Path, *, force: bool = False
) -> tuple[Path, Path]:
    """Reconcile retained evidence with a contract and persist a decision pack plus review note."""
    config = load_and_validate_config(config_path)
    evidence = load_trial_evidence(results_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    pack = assess_evidence(config, _sha256(config_path), evidence)
    stem = pack["experiment_id"]
    pack_path = output_dir / f"{stem}.decision-pack.json"
    report_path = output_dir / f"{stem}.assessment.md"
    existing = [str(path) for path in (pack_path, report_path) if path.exists()]
    if existing and not force:
        raise ConfigValidationError(
            "refusing to overwrite assessment artifacts; pass --force: " + ", ".join(existing)
        )
    _atomic_write(pack_path, json.dumps(pack, indent=2, sort_keys=True) + "\n")
    failed_gates = [gate["gate"] for gate in pack["gates"] if not gate["passed"]]
    _atomic_write(
        report_path,
        "\n".join(
            [
                f"# ACE Assessment: {stem}",
                "",
                "## Decision",
                "",
                f"- Verdict: **{pack['verdict']}**",
                f"- Config SHA-256: `{pack['config_sha256']}`",
                f"- Retained failed trials: {pack['failed_trial_count']}",
                f"- Decision pack: `{pack_path.name}`",
                "",
                "## Gaps requiring review",
                "",
                *([f"- {gap}" for gap in pack["evidence_gaps"]] or ["- None"]),
                "",
                "## Failed rule checks",
                "",
                *([f"- {gate}" for gate in failed_gates] or ["- None"]),
                "",
                "## Claim boundary",
                "",
                pack["claim_boundary"],
                "",
            ]
        ),
    )
    return pack_path, report_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ace", description="ACE experiment contract tooling")
    parser.add_argument("--version", action="version", version=f"ace {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate an ACE experiment YAML contract")
    validate.add_argument("config", type=Path)
    preflight = subparsers.add_parser(
        "preflight", help="show the evidence and execution work required before measuring"
    )
    preflight.add_argument("config", type=Path)
    run = subparsers.add_parser(
        "run", help="record a validated ACE run contract and provenance artifacts"
    )
    run.add_argument("config", type=Path)
    run.add_argument(
        "--output", required=True, type=Path, help="directory for manifest and Markdown record"
    )
    run.add_argument(
        "--force", action="store_true", help="replace existing artifacts for this experiment ID"
    )
    assess = subparsers.add_parser(
        "assess", help="reconcile retained JSON or CSV trial evidence with an ACE contract"
    )
    assess.add_argument("config", type=Path)
    assess.add_argument("results", type=Path, help="ACE trial-evidence JSON or CSV file")
    assess.add_argument(
        "--output",
        required=True,
        type=Path,
        help="directory for decision-pack and Markdown assessment",
    )
    assess.add_argument(
        "--force",
        action="store_true",
        help="replace existing assessment artifacts for this experiment ID",
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            config = load_and_validate_config(args.config)
            print(
                json.dumps(
                    {"valid": True, "experiment_id": config.get("experiment_id", args.config.stem)},
                    sort_keys=True,
                )
            )
            return 0
        if args.command == "preflight":
            config = load_and_validate_config(args.config)
            print(json.dumps(build_preflight(args.config, config), indent=2, sort_keys=True))
            return 0
        if args.command == "assess":
            pack, report = write_assessment_artifacts(
                args.config, args.results, args.output, force=args.force
            )
            print(json.dumps({"decision_pack": str(pack), "report": str(report)}, sort_keys=True))
            return 0
        manifest, report = write_run_artifacts(args.config, args.output, force=args.force)
        print(json.dumps({"manifest": str(manifest), "report": str(report)}, sort_keys=True))
        return 0
    except (ConfigValidationError, EvidenceValidationError) as exc:
        print(f"ace: validation error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
