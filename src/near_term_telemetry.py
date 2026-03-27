"""Near-term telemetry harness with hardened variance controls and provenance tracking."""

from __future__ import annotations

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import gc
import hashlib
import json
import os
import statistics
import subprocess
import time
import tracemalloc
import random

from src.benchmark_quality import score_quality


@dataclass(frozen=True)
class MeasurementProtocol:
    version: str = "near_term_protocol_v2"
    fixed_warmup_count: int = 2
    stable_measurement_windows: int = 5
    deterministic_seed_policy: str = "sha256(experiment_id, benchmark_id, trial_num, window_index)"
    run_isolation_policy: str = "gc.collect + tracemalloc reset + deterministic state rebuild per window"
    outlier_handling_policy: str = "median-centered MAD filter, keep windows with |x-median| <= 3*MAD"
    reset_sleep_ms: int = 1


PROTOCOL = MeasurementProtocol()
BASELINE_PEAK_POWER_WATTS = 285.0
CALIBRATION_FACTOR = 1.12


def run_near_term_trial(
    kernel_metrics: Dict[str, float],
    experiment_id: str,
    benchmark_id: str,
    trial_num: int,
    baseline: Dict[str, float],
) -> Dict[str, float]:
    """Execute measured workload and blend with kernel semantics."""
    benchmark_profile = _load_benchmark_profile(benchmark_id)
    runtime_ms, memory_peak_mb, tokens_processed, cpu_seconds, variance_meta = _measure_workload(
        experiment_id=experiment_id,
        benchmark_id=benchmark_id,
        trial_num=trial_num,
        benchmark_profile=benchmark_profile,
    )

    runtime_seconds = max(runtime_ms / 1000.0, 1e-9)
    throughput = tokens_processed / runtime_seconds

    energy_joules, power_watts, power_mode, power_uncertainty, power_meta = _measure_energy_and_power(
        runtime_seconds=runtime_seconds,
        cpu_seconds=cpu_seconds,
        benchmark_profile=benchmark_profile,
        baseline=baseline,
    )
    energy_uncertainty = max(energy_joules * power_uncertainty, baseline.get("energy_joules_std", 0.032))

    quality = score_quality(
        experiment_id=experiment_id,
        benchmark_id=benchmark_id,
        kernel_metrics=kernel_metrics,
        baseline_metrics=baseline,
    )
    complexity_overhead = float(kernel_metrics.get("complexity_overhead", 0.02))

    candidate_qat = quality.quality_score / max(runtime_ms * energy_joules, 1e-9)
    baseline_qat = baseline.get("accuracy", 0.9847) / max(
        baseline.get("latency_ms", 87.3) * baseline.get("energy_joules", 0.548),
        1e-9,
    )
    ecd_improvement = (candidate_qat - baseline_qat) / max(abs(baseline_qat), 1e-9)
    ecd_uncertainty = abs(ecd_improvement) * (power_uncertainty + quality.quality_uncertainty)

    metrics = {
        "accuracy": quality.quality_score,
        "accuracy_uncertainty": quality.quality_uncertainty,
        "runtime_ms": runtime_ms,
        "latency_ms": runtime_ms,
        "throughput_tok_sec": throughput,
        "memory_peak_mb": memory_peak_mb,
        "power_watts": power_watts,
        "power_watts_uncertainty": power_watts * power_uncertainty,
        "power_source_agreement_watts": float(power_meta.get("power_source_agreement_watts", 0.0)),
        "power_sample_count": float(power_meta.get("power_sample_count", 0)),
        "energy_joules": energy_joules,
        "energy_joules_uncertainty": energy_uncertainty,
        "complexity_overhead": complexity_overhead,
        "ecd_improvement": ecd_improvement,
        "ecd_improvement_uncertainty": ecd_uncertainty,
        "measurement_window_count": variance_meta["measurement_window_count"],
        "warmup_count": variance_meta["warmup_count"],
        "outlier_window_count": variance_meta["outlier_window_count"],
        "runtime_window_std_ms": variance_meta["runtime_window_std_ms"],
    }

    for metric_name in ("memory_bandwidth_reduction", "model_size_mb", "tokens_pruned", "fusion_ratio"):
        if metric_name in kernel_metrics:
            metrics[metric_name] = float(kernel_metrics[metric_name])

    metrics["measurement_dependency_map"] = json.dumps(
        {
            "formula": "ECD improvement = ((quality_score / (runtime_ms * energy_joules)) - baseline_qat) / baseline_qat",
            "inputs": {
                "quality_score": quality.provenance,
                "runtime_ms": "direct",
                "energy_joules": "derived",
                "power_watts": power_mode,
                "baseline_qat": "derived_from_baseline_snapshot",
            },
            "quality_scoring_function": quality.scoring_function,
            "dataset_inputs": quality.dataset_inputs,
            "protocol_version": PROTOCOL.version,
        }
    )
    metrics["quality_scoring_function"] = quality.scoring_function
    metrics["energy_telemetry_mode"] = power_mode
    metrics["power_aggregation_method"] = power_meta.get("aggregation_method", "")
    metrics["power_missing_data_rule"] = power_meta.get("missing_data_rule", "")
    metrics["power_sources_used"] = json.dumps(power_meta.get("sources_used", []))
    metrics["power_raw_samples_json"] = json.dumps(power_meta.get("raw_samples", {}))
    metrics["measurement_protocol_version"] = PROTOCOL.version

    metrics["metric_sources"] = {
        "runtime_ms": "direct",
        "latency_ms": "direct",
        "throughput_tok_sec": "direct",
        "memory_peak_mb": "direct",
        "power_watts": power_mode,
        "energy_joules": "derived",
        "power_source_agreement_watts": "derived",
        "power_sample_count": "direct" if power_mode == "direct" else "estimated",
        "accuracy": "benchmark-scored",
        "accuracy_uncertainty": "derived",
        "power_watts_uncertainty": "derived",
        "energy_joules_uncertainty": "derived",
        "complexity_overhead": "estimated",
        "ecd_improvement": "derived",
        "ecd_improvement_uncertainty": "derived",
        "power_aggregation_method": "derived",
        "power_missing_data_rule": "derived",
        "power_sources_used": "derived",
        "power_raw_samples_json": "derived",
        "measurement_window_count": "direct",
        "warmup_count": "direct",
        "outlier_window_count": "derived",
        "runtime_window_std_ms": "derived",
    }

    return metrics


def _measure_workload(
    experiment_id: str,
    benchmark_id: str,
    trial_num: int,
    benchmark_profile: Dict[str, object],
) -> Tuple[float, float, int, float, Dict[str, float]]:
    runtime_windows: List[float] = []
    memory_windows: List[float] = []
    cpu_windows: List[float] = []
    token_windows: List[int] = []

    warmup_runs = max(PROTOCOL.fixed_warmup_count, int(benchmark_profile.get("metadata", {}).get("warmup_runs", 0)))
    window_count = max(PROTOCOL.stable_measurement_windows, int(benchmark_profile.get("metadata", {}).get("repetitions", 1)))

    total_windows = warmup_runs + window_count
    for window_index in range(total_windows):
        seed = _stable_seed(experiment_id, benchmark_id, trial_num, window_index)
        runtime_ms, memory_peak_mb, tokens_processed, cpu_seconds = _execute_window(
            seed=seed,
            benchmark_profile=benchmark_profile,
        )
        if window_index < warmup_runs:
            continue
        runtime_windows.append(runtime_ms)
        memory_windows.append(memory_peak_mb)
        token_windows.append(tokens_processed)
        cpu_windows.append(cpu_seconds)

    filtered_indices = _filtered_window_indices(runtime_windows)
    filtered_runtime = [runtime_windows[i] for i in filtered_indices]
    filtered_memory = [memory_windows[i] for i in filtered_indices]
    filtered_cpu = [cpu_windows[i] for i in filtered_indices]
    filtered_tokens = [token_windows[i] for i in filtered_indices]

    runtime_ms = statistics.mean(filtered_runtime)
    memory_peak_mb = max(filtered_memory)
    tokens_processed = int(round(statistics.mean(filtered_tokens)))
    cpu_seconds = statistics.mean(filtered_cpu)

    variance_meta = {
        "measurement_window_count": float(window_count),
        "warmup_count": float(warmup_runs),
        "outlier_window_count": float(window_count - len(filtered_indices)),
        "runtime_window_std_ms": statistics.stdev(filtered_runtime) if len(filtered_runtime) > 1 else 0.0,
    }
    return runtime_ms, memory_peak_mb, tokens_processed, cpu_seconds, variance_meta


def _execute_window(seed: int, benchmark_profile: Dict[str, object]) -> Tuple[float, float, int, float]:
    metadata = benchmark_profile.get("metadata", {})
    input_size = benchmark_profile.get("input_size", "")
    seq_len = _extract_value(input_size, "seq_len", 128)
    batch = _extract_value(input_size, "batch", 1)

    gc.collect()
    time.sleep(PROTOCOL.reset_sleep_ms / 1000.0)

    rng = random.Random(seed)
    size = max(256, int(seq_len * 1.5 + batch * 64))
    iterations = max(4, int(metadata.get("repetitions", 3)) + batch)
    data = [rng.random() for _ in range(size)]

    tracemalloc.start()
    cpu_start = time.process_time()
    start = time.perf_counter()

    tokens_processed = 0
    for _ in range(iterations):
        for i in range(0, size, 4):
            a = data[i % size]
            b = data[(i + 1) % size]
            c = data[(i + 2) % size]
            d = data[(i + 3) % size]
            data[i % size] = (a * 0.61 + b * 0.19 + c * 0.13 + d * 0.07)
            tokens_processed += min(4, seq_len)

    elapsed_s = time.perf_counter() - start
    cpu_elapsed_s = time.process_time() - cpu_start
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return elapsed_s * 1000.0, peak / (1024.0 * 1024.0), tokens_processed, cpu_elapsed_s


def _measure_energy_and_power(
    runtime_seconds: float,
    cpu_seconds: float,
    benchmark_profile: Dict[str, object],
    baseline: Dict[str, float],
) -> Tuple[float, float, str, float, Dict[str, Any]]:
    direct, direct_meta = _read_direct_power_watts(runtime_seconds)
    if direct is not None:
        energy = direct * runtime_seconds
        return energy, direct, "direct", 0.05, direct_meta

    baseline_latency_ms = float(baseline.get("latency_ms", baseline.get("latency_ms_mean", 87.3)))
    baseline_energy = float(baseline.get("energy_joules", baseline.get("energy_joules_mean", 0.548)))
    runtime_ms = runtime_seconds * 1000.0
    utilization = min(1.1, max(0.85, cpu_seconds / max(runtime_seconds, 1e-9)))
    batch_scale = 1.0 + (_extract_value(benchmark_profile.get("input_size", ""), "batch", 1) - 1) * 0.06
    energy_scale = (runtime_ms / max(baseline_latency_ms, 1e-9)) * (0.92 + 0.05 * batch_scale + 0.03 * utilization)
    calibrated_energy = max(0.02, baseline_energy * energy_scale * CALIBRATION_FACTOR)
    calibrated_power = calibrated_energy / max(runtime_seconds, 1e-9)
    calibrated_power = min(BASELINE_PEAK_POWER_WATTS, max(10.0, calibrated_power))
    calibrated_energy = calibrated_power * runtime_seconds
    return calibrated_energy, calibrated_power, "estimated", 0.10, {
        "aggregation_method": "calibrated_runtime_proxy",
        "missing_data_rule": "When direct device telemetry is unavailable, use baseline-calibrated runtime proxy with bounded uncertainty.",
        "sources_used": ["runtime_seconds", "cpu_seconds", "benchmark_batch_scale", "baseline_energy"],
        "raw_samples": {},
        "power_source_agreement_watts": 0.0,
        "power_sample_count": 0,
    }


def _read_direct_power_watts(runtime_seconds: float) -> Tuple[float | None, Dict[str, Any]]:
    env_value = os.getenv("ACE_DIRECT_POWER_WATTS")
    if env_value:
        try:
            value = float(env_value)
            return value, {
                "aggregation_method": "env_override_single_value",
                "missing_data_rule": "ACE_DIRECT_POWER_WATTS override used when device telemetry source is externally provided.",
                "sources_used": ["ACE_DIRECT_POWER_WATTS"],
                "raw_samples": {"ACE_DIRECT_POWER_WATTS": [value]},
                "power_source_agreement_watts": 0.0,
                "power_sample_count": 1,
            }
        except ValueError:
            pass

    source_commands = {
        "nvidia_power_draw": ["nvidia-smi", "--query-gpu=power.draw", "--format=csv,noheader,nounits"],
        "nvidia_power_draw_avg": ["nvidia-smi", "--query-gpu=power.draw.average", "--format=csv,noheader,nounits"],
        "nvidia_power_draw_inst": ["nvidia-smi", "--query-gpu=power.draw.instant", "--format=csv,noheader,nounits"],
    }

    sample_interval = min(0.1, max(0.02, runtime_seconds / 5.0))
    target_samples = max(3, int(max(runtime_seconds, 0.2) / sample_interval))
    raw_samples: Dict[str, List[float]] = {k: [] for k in source_commands.keys()}

    for _ in range(target_samples):
        for source_name, command in source_commands.items():
            value = _sample_power_command(command)
            if value is not None:
                raw_samples[source_name].append(value)
        time.sleep(sample_interval)

    source_medians: Dict[str, float] = {
        source: statistics.median(values)
        for source, values in raw_samples.items()
        if values
    }
    if not source_medians:
        return None, {
            "aggregation_method": "no_direct_source_available",
            "missing_data_rule": "If all direct telemetry sources fail, fallback to calibrated proxy path.",
            "sources_used": [],
            "raw_samples": raw_samples,
            "power_source_agreement_watts": 0.0,
            "power_sample_count": 0,
        }

    reconciled = statistics.median(source_medians.values())
    agreement = statistics.stdev(source_medians.values()) if len(source_medians) > 1 else 0.0
    power_sample_count = sum(len(v) for v in raw_samples.values())
    return reconciled, {
        "aggregation_method": "median_of_source_medians(nvidia_power_draw, nvidia_power_draw_avg, nvidia_power_draw_inst)",
        "missing_data_rule": "Drop missing source samples; require at least one non-empty source. If none available, fallback to calibrated proxy.",
        "sources_used": sorted(source_medians.keys()),
        "raw_samples": raw_samples,
        "power_source_agreement_watts": float(agreement),
        "power_sample_count": int(power_sample_count),
    }


def _sample_power_command(command: List[str]) -> float | None:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=1.0, check=True)
        lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        if not lines:
            return None
        return float(lines[0].split()[0])
    except Exception:
        return None


def _filtered_window_indices(values: List[float]) -> List[int]:
    if len(values) < 3:
        return list(range(len(values)))
    median = statistics.median(values)
    deviations = [abs(v - median) for v in values]
    mad = statistics.median(deviations)
    if mad == 0:
        return list(range(len(values)))
    threshold = 3.0 * mad
    return [idx for idx, value in enumerate(values) if abs(value - median) <= threshold]


def _stable_seed(experiment_id: str, benchmark_id: str, trial_num: int, window_index: int) -> int:
    digest = hashlib.sha256(
        f"{experiment_id}|{benchmark_id}|{trial_num}|{window_index}".encode("utf-8")
    ).hexdigest()
    return int(digest[:16], 16)


def _load_benchmark_profile(benchmark_id: str) -> Dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    path = root / "configs" / "benchmarks" / f"{benchmark_id}.yaml"
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _extract_value(input_size: str, key: str, default: int) -> int:
    for part in str(input_size).split(","):
        part = part.strip()
        if part.startswith(f"{key}="):
            try:
                return int(part.split("=", 1)[1])
            except ValueError:
                return default
    return default