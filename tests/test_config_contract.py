from pathlib import Path

import yaml


REQUIRED_KEYS = [
    "baseline",
    "mutation_scope",
    "trials",
    "quality_floor",
    "benchmark_sets",
    "acceptance",
    "reporting",
]


def test_all_experiment_configs_have_required_contract():
    root = Path(__file__).resolve().parents[1]
    exp_dir = root / "experiments"

    yaml_files = sorted(exp_dir.rglob("*.yaml"))
    assert yaml_files, "No experiment YAML files found"

    missing = []
    for path in yaml_files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for key in REQUIRED_KEYS:
            if key not in data:
                missing.append((str(path), key))

    assert not missing, f"Missing required keys: {missing}"


def test_holdout_present_in_benchmark_sets():
    root = Path(__file__).resolve().parents[1]
    yaml_files = sorted((root / "experiments").rglob("*.yaml"))

    bad = []
    for path in yaml_files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        bsets = data.get("benchmark_sets", {})
        holdout = bsets.get("holdout", [])
        if not holdout:
            bad.append(str(path))

    assert not bad, f"Missing holdout benchmark definitions: {bad}"
