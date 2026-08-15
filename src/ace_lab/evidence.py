"""Import retained trial evidence and reconcile it against an ACE contract.

This module deliberately does not execute a workload or manufacture a result.  Its job is to
make a reviewable decision pack from evidence the user already retained.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import statistics
from pathlib import Path
from typing import Any

from ace_lab import __version__


EVIDENCE_SCHEMA_VERSION = "1.0"
REQUIRED_SPLITS = ("development", "validation", "holdout")
ALLOWED_PROVENANCE = {"measured", "estimated", "simulated"}


class EvidenceValidationError(ValueError):
    """Raised when a retained evidence file cannot be safely interpreted."""


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.lower() in {"true", "false"}:
        return value.lower() == "true"
    raise EvidenceValidationError("success must be true or false")


def _decode_object(value: str | None, column: str) -> dict[str, Any]:
    if not value:
        return {}
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as exc:
        raise EvidenceValidationError(f"CSV {column} must contain a JSON object") from exc
    if not isinstance(decoded, dict):
        raise EvidenceValidationError(f"CSV {column} must contain a JSON object")
    return decoded


def _read_csv(path: Path) -> dict[str, Any]:
    """Import a portable CSV form with repeated metadata on every row."""
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise EvidenceValidationError("CSV evidence must contain at least one data row")
    required = {
        "experiment_id",
        "config_sha256",
        "source_revision",
        "telemetry_provenance",
        "trial_id",
        "seed",
        "split",
        "success",
        "metrics_json",
        "metric_sources_json",
    }
    headers = set(rows[0] or {})
    missing = sorted(required - headers)
    if missing:
        raise EvidenceValidationError("CSV missing required columns: " + ", ".join(missing))

    def metadata(name: str) -> str:
        values = {row.get(name, "") for row in rows}
        if len(values) != 1 or not next(iter(values)):
            raise EvidenceValidationError(
                f"CSV {name} must have one non-empty value across all rows"
            )
        return next(iter(values))

    return {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "artifact_type": "ace-trial-evidence",
        "experiment_id": metadata("experiment_id"),
        "config_sha256": metadata("config_sha256"),
        "source_revision": metadata("source_revision"),
        "telemetry_provenance": metadata("telemetry_provenance"),
        "baseline_metrics": _decode_object(
            rows[0].get("baseline_metrics_json"), "baseline_metrics_json"
        ),
        "statistical_evidence": _decode_object(
            rows[0].get("statistical_evidence_json"), "statistical_evidence_json"
        ),
        "trials": [
            {
                "trial_id": row["trial_id"],
                "seed": int(row["seed"]),
                "split": row["split"],
                "success": _as_bool(row["success"]),
                "metrics": _decode_object(row["metrics_json"], "metrics_json"),
                "metric_sources": _decode_object(row["metric_sources_json"], "metric_sources_json"),
                "error_message": row.get("error_message", ""),
            }
            for row in rows
        ],
    }


def load_trial_evidence(path: Path) -> dict[str, Any]:
    """Load JSON or CSV trial evidence without running any experiment."""
    if not path.is_file():
        raise EvidenceValidationError(f"results do not exist: {path}")
    if path.suffix.lower() == ".csv":
        data = _read_csv(path)
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            raise EvidenceValidationError(f"invalid JSON evidence: {exc}") from exc
    if not isinstance(data, dict):
        raise EvidenceValidationError("evidence must contain a JSON object")
    _validate_evidence_shape(data)
    return data


def _validate_evidence_shape(data: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "artifact_type",
        "experiment_id",
        "config_sha256",
        "source_revision",
        "telemetry_provenance",
        "baseline_metrics",
        "trials",
    }
    missing = sorted(required - set(data))
    if missing:
        raise EvidenceValidationError("evidence missing required fields: " + ", ".join(missing))
    if (
        data["schema_version"] != EVIDENCE_SCHEMA_VERSION
        or data["artifact_type"] != "ace-trial-evidence"
    ):
        raise EvidenceValidationError("unsupported ACE trial-evidence schema")
    if data["telemetry_provenance"] not in ALLOWED_PROVENANCE:
        raise EvidenceValidationError(
            "telemetry_provenance must be measured, estimated, or simulated"
        )
    if not isinstance(data["baseline_metrics"], dict):
        raise EvidenceValidationError("baseline_metrics must be an object")
    if not isinstance(data["trials"], list) or not data["trials"]:
        raise EvidenceValidationError("trials must be a non-empty list")
    identifiers: set[str] = set()
    for index, trial in enumerate(data["trials"], start=1):
        if not isinstance(trial, dict):
            raise EvidenceValidationError(f"trial {index} must be an object")
        needed = {"trial_id", "seed", "split", "success", "metrics", "metric_sources"}
        absent = sorted(needed - set(trial))
        if absent:
            raise EvidenceValidationError(f"trial {index} missing: " + ", ".join(absent))
        if str(trial["trial_id"]) in identifiers:
            raise EvidenceValidationError(f"duplicate trial_id: {trial['trial_id']}")
        identifiers.add(str(trial["trial_id"]))
        if trial["split"] not in REQUIRED_SPLITS:
            raise EvidenceValidationError(f"trial {index} has unsupported split: {trial['split']}")
        if isinstance(trial["seed"], bool) or not isinstance(trial["seed"], int):
            raise EvidenceValidationError(f"trial {index} seed must be an integer")
        if not isinstance(trial["success"], bool):
            raise EvidenceValidationError(f"trial {index} success must be boolean")
        if not isinstance(trial["metrics"], dict) or not isinstance(trial["metric_sources"], dict):
            raise EvidenceValidationError(
                f"trial {index} metrics and metric_sources must be objects"
            )
        if not trial["success"] and not trial.get("error_message"):
            raise EvidenceValidationError(
                f"failed trial {trial['trial_id']} must retain error_message"
            )


def _numeric_mean(trials: list[dict[str, Any]], metric: str) -> float | None:
    values = [trial["metrics"].get(metric) for trial in trials]
    if not values or any(
        isinstance(value, bool) or not isinstance(value, (int, float)) for value in values
    ):
        return None
    return float(statistics.mean(values))


def _gate(name: str, passed: bool, **evidence: Any) -> dict[str, Any]:
    return {"gate": name, "passed": passed, "evidence": evidence}


def assess_evidence(
    config: dict[str, Any], config_sha256: str, evidence: dict[str, Any]
) -> dict[str, Any]:
    """Reconcile retained evidence with a contract and emit no stronger verdict than justified."""
    trial_config = config.get("trial_configuration", {})
    declared_seeds = set(trial_config.get("seeds", []))
    expected_trials = int(config["trials"])
    experiment_id = config.get("experiment_id")
    quality_metric = config["quality_floor"].get("metric", "accuracy")
    minimum_relative = float(config["quality_floor"].get("minimum_relative_to_baseline", 1.0))
    minimum_ecd = float(config["acceptance"].get("minimum_ecd_improvement", 0.0))
    maximum_complexity = config["acceptance"].get("maximum_complexity_overhead")
    successful = [trial for trial in evidence["trials"] if trial["success"]]
    failed = [trial for trial in evidence["trials"] if not trial["success"]]
    gates: list[dict[str, Any]] = []
    gaps: list[str] = []

    contract_trial_plan_ok = bool(declared_seeds) and len(declared_seeds) == expected_trials
    gates.append(
        _gate(
            "contract_trial_plan",
            contract_trial_plan_ok,
            declared_trials=expected_trials,
            declared_seed_count=len(declared_seeds),
        )
    )
    if not contract_trial_plan_ok:
        gaps.append("The contract's declared trial count and explicit seed plan do not reconcile.")
    gates.append(
        _gate(
            "experiment_identity",
            evidence["experiment_id"] == experiment_id,
            expected=experiment_id,
            actual=evidence["experiment_id"],
        )
    )
    gates.append(
        _gate(
            "config_digest",
            evidence["config_sha256"] == config_sha256,
            expected=config_sha256,
            actual=evidence["config_sha256"],
        )
    )
    expected_provenance = config.get("telemetry_provenance")
    provenance_ok = (
        bool(expected_provenance) and evidence["telemetry_provenance"] == expected_provenance
    )
    gates.append(
        _gate(
            "telemetry_provenance",
            provenance_ok,
            expected=expected_provenance,
            actual=evidence["telemetry_provenance"],
        )
    )
    if not expected_provenance:
        gaps.append("The contract does not declare telemetry provenance.")
    if not evidence.get("source_revision"):
        gaps.append("Evidence does not retain a source revision.")
    gates.append(
        _gate(
            "source_revision_retained",
            bool(evidence.get("source_revision")),
            actual=evidence.get("source_revision"),
        )
    )

    split_summary: dict[str, dict[str, Any]] = {}
    for split in REQUIRED_SPLITS:
        split_success = [trial for trial in successful if trial["split"] == split]
        split_failed = [trial for trial in failed if trial["split"] == split]
        observed_seeds = {trial["seed"] for trial in split_success}
        missing_seeds = sorted(declared_seeds - observed_seeds)
        metrics = {
            metric: _numeric_mean(split_success, metric)
            for metric in (quality_metric, "ecd_improvement", "complexity_overhead")
        }
        split_summary[split] = {
            "successful_trials": len(split_success),
            "failed_trials": len(split_failed),
            "observed_seeds": sorted(observed_seeds),
            "missing_declared_seeds": missing_seeds,
            "means": metrics,
        }
        complete = len(split_success) >= expected_trials and not missing_seeds
        gates.append(
            _gate(
                f"{split}_trial_coverage",
                complete,
                required_trials=expected_trials,
                actual_successful_trials=len(split_success),
                missing_declared_seeds=missing_seeds,
            )
        )
        if not complete:
            gaps.append(
                f"{split} does not contain the declared successful-trial and seed coverage."
            )
        if any(value is None for value in metrics.values()):
            gaps.append(f"{split} is missing one or more required numeric metrics.")

    baseline_quality = evidence["baseline_metrics"].get(quality_metric)
    if isinstance(baseline_quality, bool) or not isinstance(baseline_quality, (int, float)):
        gaps.append(f"Baseline {quality_metric} is missing from retained evidence.")
        quality_floor = None
    else:
        quality_floor = float(baseline_quality) * minimum_relative
    for split in REQUIRED_SPLITS:
        mean_quality = split_summary[split]["means"][quality_metric]
        gates.append(
            _gate(
                f"{split}_quality_floor",
                quality_floor is not None
                and mean_quality is not None
                and mean_quality >= quality_floor,
                required=quality_floor,
                actual=mean_quality,
            )
        )

    gates.append(
        _gate(
            "development_minimum_ecd",
            split_summary["development"]["means"]["ecd_improvement"] is not None
            and split_summary["development"]["means"]["ecd_improvement"] >= minimum_ecd,
            required=minimum_ecd,
            actual=split_summary["development"]["means"]["ecd_improvement"],
        )
    )
    for split, required in (
        ("validation", config["acceptance"].get("require_validation_transfer", False)),
        ("holdout", config["acceptance"].get("require_holdout_pass", False)),
    ):
        mean_ecd = split_summary[split]["means"]["ecd_improvement"]
        gates.append(
            _gate(
                f"{split}_minimum_ecd",
                (not required) or (mean_ecd is not None and mean_ecd >= minimum_ecd),
                required=bool(required),
                threshold=minimum_ecd,
                actual=mean_ecd,
            )
        )
    if maximum_complexity is not None:
        actual = split_summary["development"]["means"]["complexity_overhead"]
        gates.append(
            _gate(
                "development_complexity_overhead",
                actual is not None and actual <= float(maximum_complexity),
                required=float(maximum_complexity),
                actual=actual,
            )
        )

    stats_evidence = evidence.get("statistical_evidence", {})
    if config["acceptance"].get("require_statistical_significance", False):
        p_value = (
            stats_evidence.get("development", {}).get("p_value")
            if isinstance(stats_evidence, dict)
            else None
        )
        gates.append(
            _gate(
                "development_statistical_significance",
                isinstance(p_value, (int, float)) and p_value < 0.05,
                required="p_value < 0.05",
                actual=p_value,
            )
        )
        if not isinstance(p_value, (int, float)):
            gaps.append("Development statistical evidence is required but no p_value was retained.")
    if config["acceptance"].get("confidence_interval_excludes_zero", False):
        ci = (
            stats_evidence.get("development", {}).get("ecd_confidence_interval")
            if isinstance(stats_evidence, dict)
            else None
        )
        ci_ok = (
            isinstance(ci, list)
            and len(ci) == 2
            and all(isinstance(value, (int, float)) for value in ci)
            and not (ci[0] <= 0 <= ci[1])
        )
        gates.append(
            _gate(
                "development_confidence_interval", ci_ok, required="ECD CI excludes zero", actual=ci
            )
        )
        if not isinstance(ci, list):
            gaps.append("Development ECD confidence interval is required but not retained.")

    identity_gate_names = {
        "contract_trial_plan",
        "experiment_identity",
        "config_digest",
        "telemetry_provenance",
        "source_revision_retained",
    }
    identity_ok = all(gate["passed"] for gate in gates if gate["gate"] in identity_gate_names)
    coverage_ok = not gaps
    if not identity_ok or not coverage_ok:
        verdict = "INCONCLUSIVE"
        reasons = ["Evidence is incomplete or does not reconcile with the declared contract."]
    elif all(gate["passed"] for gate in gates):
        verdict = "ACCEPTED"
        reasons = [
            "Retained evidence satisfies the configured rule checks. Independent reproduction is still outside this assessment."
        ]
    else:
        verdict = "REJECTED"
        reasons = ["Retained evidence is complete but fails one or more declared acceptance rules."]
    return {
        "schema_version": "1.0",
        "artifact_type": "ace-decision-pack",
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "package_version": __version__,
        "experiment_id": experiment_id,
        "config_sha256": config_sha256,
        "source_revision": evidence.get("source_revision"),
        "evidence_schema_version": evidence["schema_version"],
        "verdict": verdict,
        "reasons": reasons,
        "evidence_gaps": sorted(set(gaps)),
        "failed_trial_count": len(failed),
        "split_summary": split_summary,
        "gates": gates,
        "claim_boundary": "This decision pack reconciles retained, user-supplied evidence against an ACE contract. It does not execute a workload, attest to data collection, independently reproduce a result, or certify deployment safety.",
    }
