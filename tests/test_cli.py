import json
from pathlib import Path

from ace_lab.cli import main


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


def test_validate_rejects_missing_holdout(tmp_path: Path, capsys):
    config = tmp_path / "bad.yaml"
    config.write_text(_valid_config().replace("  holdout: [holdout]\n", ""), encoding="utf-8")
    assert main(["validate", str(config)]) == 2
    assert "holdout" in capsys.readouterr().err


def test_validate_rejects_unsafe_experiment_id(tmp_path: Path, capsys):
    config = tmp_path / "bad.yaml"
    config.write_text(_valid_config().replace("experiment_id: smoke", "experiment_id: ../escape"), encoding="utf-8")
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
    assert "INCONCLUSIVE" in report


def test_run_refuses_to_replace_existing_artifacts_without_force(tmp_path: Path, capsys):
    config = tmp_path / "experiment.yaml"
    output = tmp_path / "out"
    config.write_text(_valid_config(), encoding="utf-8")
    assert main(["run", str(config), "--output", str(output)]) == 0
    assert main(["run", str(config), "--output", str(output)]) == 2
    assert "refusing to overwrite" in capsys.readouterr().err
    assert main(["run", str(config), "--output", str(output), "--force"]) == 0
