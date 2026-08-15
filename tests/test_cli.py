import json
import hashlib
from pathlib import Path

from ace_lab.cli import main
from ace_lab.evidence import load_trial_evidence


def _valid_config() -> str:
    return """
experiment_id: smoke
baseline: baseline-v1
mutation_scope: [quantization]
trials: 2
quality_floor: {metric: accuracy, minimum_relative_to_baseline: 0.99}
benchmark_sets:
  development: [dev]
  validation: [validation]
  holdout: [holdout]
acceptance: {confidence_level: 0.95}
reporting: {report_format: [json, markdown]}
trial_configuration: {seeds: [42, 99]}
telemetry_provenance: simulated
"""


def test_validate_accepts_complete_contract(tmp_path: Path, capsys):
    config = tmp_path / "experiment.yaml"
    config.write_text(_valid_config(), encoding="utf-8")
    assert main(["validate", str(config)]) == 0
    assert json.loads(capsys.readouterr().out)["valid"] is True


def test_preflight_turns_a_contract_into_specific_next_actions(tmp_path: Path, capsys):
    config = tmp_path / "experiment.yaml"
    config.write_text(_valid_config(), encoding="utf-8")
    assert main(["preflight", str(config)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ready_to_measure"] is True
    assert output["split_counts"] == {"development": 1, "holdout": 1, "validation": 1}
    assert len(output["next_actions"]) == 5


def test_preflight_surfaces_seed_and_telemetry_gaps(tmp_path: Path, capsys):
    config = tmp_path / "experiment.yaml"
    config.write_text(
        _valid_config()
        .replace("trial_configuration: {seeds: [42, 99]}\n", "")
        .replace("telemetry_provenance: simulated\n", ""),
        encoding="utf-8",
    )
    assert main(["preflight", str(config)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ready_to_measure"] is False
    assert len(output["warnings"]) == 2


def test_validate_rejects_missing_holdout(tmp_path: Path, capsys):
    config = tmp_path / "bad.yaml"
    config.write_text(_valid_config().replace("  holdout: [holdout]\n", ""), encoding="utf-8")
    assert main(["validate", str(config)]) == 2
    assert "holdout" in capsys.readouterr().err


def test_validate_rejects_unsafe_experiment_id(tmp_path: Path, capsys):
    config = tmp_path / "bad.yaml"
    config.write_text(
        _valid_config().replace("experiment_id: smoke", "experiment_id: ../escape"),
        encoding="utf-8",
    )
    assert main(["validate", str(config)]) == 2
    assert "experiment_id" in capsys.readouterr().err


def test_run_writes_manifest_and_inconclusive_record(tmp_path: Path):
    config = tmp_path / "experiment.yaml"
    output = tmp_path / "out"
    config.write_text(_valid_config(), encoding="utf-8")
    assert main(["run", str(config), "--output", str(output)]) == 0
    manifest = json.loads((output / "smoke.manifest.json").read_text(encoding="utf-8"))
    report = (output / "smoke.report.md").read_text(encoding="utf-8")
    assert manifest["schema_version"] == "1.0"
    assert manifest["execution_mode"] == "contract-recording-only"
    assert manifest["verdict"] == "inconclusive"
    assert manifest["preflight"]["ready_to_measure"] is True
    assert "INCONCLUSIVE" in report
    assert "What to do next" in report


def test_run_refuses_to_replace_existing_artifacts_without_force(tmp_path: Path, capsys):
    config = tmp_path / "experiment.yaml"
    output = tmp_path / "out"
    config.write_text(_valid_config(), encoding="utf-8")
    assert main(["run", str(config), "--output", str(output)]) == 0
    assert main(["run", str(config), "--output", str(output)]) == 2
    assert "refusing to overwrite" in capsys.readouterr().err
    assert main(["run", str(config), "--output", str(output), "--force"]) == 0


def _evidence(config: Path) -> dict:
    digest = hashlib.sha256(config.read_bytes()).hexdigest()
    trials = []
    for split in ("development", "validation", "holdout"):
        for seed in (42, 99):
            trials.append(
                {
                    "trial_id": f"{split}-{seed}",
                    "seed": seed,
                    "split": split,
                    "success": True,
                    "metrics": {
                        "accuracy": 0.995,
                        "ecd_improvement": 0.2,
                        "complexity_overhead": 0.01,
                    },
                    "metric_sources": {
                        "accuracy": "measured",
                        "ecd_improvement": "measured",
                        "complexity_overhead": "measured",
                    },
                }
            )
    return {
        "schema_version": "1.0",
        "artifact_type": "ace-trial-evidence",
        "experiment_id": "smoke",
        "config_sha256": digest,
        "source_revision": "abc123",
        "telemetry_provenance": "simulated",
        "baseline_metrics": {"accuracy": 1.0},
        "trials": trials,
    }


def test_assess_writes_accepted_reviewable_decision_pack(tmp_path: Path):
    config = tmp_path / "experiment.yaml"
    results = tmp_path / "retained-trials.json"
    output = tmp_path / "assessment"
    config.write_text(_valid_config(), encoding="utf-8")
    results.write_text(json.dumps(_evidence(config)), encoding="utf-8")
    assert main(["assess", str(config), str(results), "--output", str(output)]) == 0
    pack = json.loads((output / "smoke.decision-pack.json").read_text(encoding="utf-8"))
    report = (output / "smoke.assessment.md").read_text(encoding="utf-8")
    assert pack["verdict"] == "ACCEPTED"
    assert pack["evidence_gaps"] == []
    assert "This decision pack reconciles retained" in pack["claim_boundary"]
    assert "ACCEPTED" in report


def test_assess_marks_digest_mismatch_inconclusive_without_silently_fixing_it(tmp_path: Path):
    config = tmp_path / "experiment.yaml"
    results = tmp_path / "retained-trials.json"
    output = tmp_path / "assessment"
    config.write_text(_valid_config(), encoding="utf-8")
    evidence = _evidence(config)
    evidence["config_sha256"] = "0" * 64
    results.write_text(json.dumps(evidence), encoding="utf-8")
    assert main(["assess", str(config), str(results), "--output", str(output)]) == 0
    pack = json.loads((output / "smoke.decision-pack.json").read_text(encoding="utf-8"))
    assert pack["verdict"] == "INCONCLUSIVE"
    assert any(gate["gate"] == "config_digest" and not gate["passed"] for gate in pack["gates"])


def test_assess_rejects_an_internally_inconsistent_seed_plan(tmp_path: Path):
    config = tmp_path / "experiment.yaml"
    results = tmp_path / "retained-trials.json"
    output = tmp_path / "assessment"
    config.write_text(_valid_config().replace("trials: 2", "trials: 3"), encoding="utf-8")
    results.write_text(json.dumps(_evidence(config)), encoding="utf-8")
    assert main(["assess", str(config), str(results), "--output", str(output)]) == 0
    pack = json.loads((output / "smoke.decision-pack.json").read_text(encoding="utf-8"))
    assert pack["verdict"] == "INCONCLUSIVE"
    assert any(
        gate["gate"] == "contract_trial_plan" and not gate["passed"] for gate in pack["gates"]
    )


def test_csv_evidence_importer_preserves_failed_trials(tmp_path: Path):
    csv_path = tmp_path / "trials.csv"
    csv_path.write_text(
        "experiment_id,config_sha256,source_revision,telemetry_provenance,trial_id,seed,split,success,metrics_json,metric_sources_json,error_message,baseline_metrics_json,statistical_evidence_json\n"
        "smoke,"
        + "a" * 64
        + ',abc,measured,failed-1,42,development,false,{"accuracy": 0.9},{"accuracy": "measured"},timeout,{"accuracy": 1.0},{}\n',
        encoding="utf-8",
    )
    evidence = load_trial_evidence(csv_path)
    assert evidence["trials"][0]["success"] is False
    assert evidence["trials"][0]["error_message"] == "timeout"
