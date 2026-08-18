"""Regression coverage for the published Token-Bleed claim-scoped reference shape."""

import hashlib

from ace_lab.evidence import assess_evidence
from ace_lab.cli import load_and_validate_config


EXPECTED_R3 = {
    "selective_context_cost_vs_full": "ACCEPTED",
    "governed_quality_vs_full": "ACCEPTED",
    "governed_value_vs_lexical": "REJECTED",
    "governed_sensitivity_vs_lexical": "REJECTED",
}
EXPECTED_R5 = EXPECTED_R3


def _config(tmp_path, name: str):
    path = tmp_path / f"{name}.yaml"
    path.write_text(
        f"""
experiment_id: {name}
baseline: ungoverned-context-stuffing
mutation_scope: [governed-context-selection]
trials: 2
quality_floor: {{metric: f1, minimum_relative_to_baseline: 0.98}}
benchmark_sets:
  development: [tier-300]
  validation: [tier-800]
  holdout: [tier-1200]
acceptance: {{minimum_ecd_improvement: 0.0}}
reporting: {{report_format: [json]}}
trial_configuration: {{seeds: [101, 102]}}
telemetry_provenance: measured
claim_scopes:
  selective_context_cost_vs_full: {{comparison: governed-vs-ungoverned}}
  governed_quality_vs_full: {{comparison: governed-vs-ungoverned}}
  governed_value_vs_lexical: {{comparison: governed-vs-lexical}}
  governed_sensitivity_vs_lexical: {{comparison: governed-vs-lexical}}
""".lstrip(),
        encoding="utf-8",
    )
    return path, load_and_validate_config(path)


def _evidence(config_path, experiment_id: str):
    digest = hashlib.sha256(config_path.read_bytes()).hexdigest()
    trials = []
    for split in ("development", "validation", "holdout"):
        for seed in (101, 102):
            trials.append(
                {
                    "trial_id": f"{split}-{seed}",
                    "seed": seed,
                    "split": split,
                    "success": True,
                    "metrics": {"f1": 1.0, "ecd_improvement": 0.1, "complexity_overhead": 0.0},
                    "metric_sources": {
                        "f1": "measured",
                        "ecd_improvement": "measured",
                        "complexity_overhead": "measured",
                    },
                }
            )
    return {
        "schema_version": "1.0",
        "artifact_type": "ace-trial-evidence",
        "experiment_id": experiment_id,
        "config_sha256": digest,
        "source_revision": "published-reference-fixture",
        "telemetry_provenance": "measured",
        "baseline_metrics": {"f1": 1.0},
        "trials": trials,
        "claim_scoped_verdicts": {
            name: {"verdict": verdict, "checks": []}
            for name, verdict in EXPECTED_R3.items()
        },
    }


def test_public_r3_and_r5_claim_boundaries_remain_independently_reported(tmp_path):
    """Do not silently collapse an accepted generic verdict over rejected lexical claims."""
    for reference, expected in (("token-bleed-r3", EXPECTED_R3), ("token-bleed-r5", EXPECTED_R5)):
        path, config = _config(tmp_path, reference)
        pack = assess_evidence(config, hashlib.sha256(path.read_bytes()).hexdigest(), _evidence(path, reference))
        observed = {
            name: assessment["verdict"]
            for name, assessment in pack["claim_scoped_assessments"].items()
        }
        assert pack["verdict"] == "ACCEPTED"
        assert observed == expected
