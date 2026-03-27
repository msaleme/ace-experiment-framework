"""Helpers for loading YAML configs into core model/registry types."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import yaml

from src.model import Hardware, Benchmark, WorkloadClass
from src.baseline_manager import BaselineManager
from src.benchmark_registry import BenchmarkRegistry


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_baseline_from_yaml(baseline_manager: BaselineManager, yaml_path: Path) -> str:
    """Create immutable JSON baseline from YAML snapshot if missing."""
    data = load_yaml(yaml_path)
    baseline_id = data["baseline_id"]

    existing = baseline_manager.get_baseline(baseline_id)
    if existing:
        return baseline_id

    hw = data["hardware"]
    hardware = Hardware(
        name=hw["name"],
        device_type=hw["device_type"],
        model=hw["model"],
        arch=hw["arch"],
        cores=int(hw["cores"]),
        memory_gb=float(hw["memory_gb"]),
        peak_power_watts=float(hw.get("peak_power_watts", 0.0)),
        metadata={
            "peak_bandwidth_gbs": hw.get("peak_bandwidth_gbs", 0.0),
        },
    )

    bm = data["benchmark"]
    benchmark = Benchmark(
        benchmark_id=bm["benchmark_id"],
        name=bm["name"],
        workload_class=WorkloadClass(bm["workload_class"]),
        input_size=bm["input_size"],
        primary_metrics=bm.get("primary_metrics", []),
        secondarty_metrics=bm.get("secondary_metrics", []),
        quality_metric=bm.get("quality_metric", "accuracy"),
        metadata={},
        version=str(bm.get("version", "1.0")),
    )

    dependency_versions = data.get("dependency_versions", {})
    environment = data.get("environment_variables", {})

    baseline = baseline_manager.create_baseline(
        baseline_id=baseline_id,
        hardware=hardware,
        benchmark=benchmark,
        code_commit=data.get("code_commit", "unknown"),
        compiler_version=data.get("compiler_version", "unknown"),
        dependency_versions={k: str(v) for k, v in dependency_versions.items()},
        environment={k: str(v) for k, v in environment.items()},
        measurement_method=data.get("measurement_method", ""),
        seed_policy=data.get("seed_policy", "fixed_seed_only"),
        notes=data.get("notes", ""),
    )

    # Preserve measured baseline values in metadata for evaluation.
    baseline.hardware.metadata["baseline_measurements"] = data.get("baseline_measurements", {})
    return baseline.baseline_id


def ensure_benchmark_from_yaml(registry: BenchmarkRegistry, yaml_path: Path) -> str:
    """Register benchmark from YAML if missing in immutable registry."""
    data = load_yaml(yaml_path)
    benchmark_id = data["benchmark_id"]
    if registry.check_benchmark_exists(benchmark_id):
        return benchmark_id

    registry.register_benchmark(
        benchmark_id=benchmark_id,
        name=data["name"],
        workload_class=WorkloadClass(data["workload_class"]),
        input_size=data["input_size"],
        primary_metrics=data.get("primary_metrics", []),
        quality_metric=data.get("quality_metric", "accuracy"),
        secondary_metrics=data.get("secondary_metrics", []),
        version=str(data.get("version", "1.0")),
        metadata=data.get("metadata", {}),
        benchmark_set=data.get("benchmark_set", "development"),
    )
    return benchmark_id
