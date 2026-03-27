from src.benchmark_quality import score_quality
from src.near_term_telemetry import run_near_term_trial


BASELINE = {
    "accuracy": 0.9847,
    "accuracy_mean": 0.9847,
    "latency_ms": 87.3,
    "energy_joules": 0.548,
    "energy_joules_std": 0.032,
}


def test_token_pruning_quality_is_benchmark_scored():
    result = score_quality(
        experiment_id="exp_002_token_pruning",
        benchmark_id="transformer_inference_small",
        kernel_metrics={"pruning_ratio": 0.20, "tokens_pruned": 103},
        baseline_metrics=BASELINE,
    )

    assert result.provenance == "benchmark-scored"
    assert result.quality_score > 0.0
    assert result.dataset_inputs
    assert "quality_score" in result.scoring_function


def test_near_term_trial_emits_uncertainty_and_provenance():
    metrics = run_near_term_trial(
        kernel_metrics={
            "pruning_ratio": 0.20,
            "tokens_pruned": 103,
            "complexity_overhead": 0.02,
        },
        experiment_id="exp_002_token_pruning",
        benchmark_id="transformer_inference_small",
        trial_num=1,
        baseline=BASELINE,
    )

    assert metrics["energy_joules"] > 0.0
    assert metrics["energy_joules_uncertainty"] > 0.0
    assert metrics["measurement_window_count"] >= 3
    assert metrics["warmup_count"] >= 2
    assert metrics["metric_sources"]["accuracy"] == "benchmark-scored"
    assert metrics["metric_sources"]["energy_joules"] == "derived"
    assert "power_raw_samples_json" in metrics
    assert "power_aggregation_method" in metrics
    assert "power_missing_data_rule" in metrics


def test_near_term_trial_direct_power_override(monkeypatch):
    monkeypatch.setenv("ACE_DIRECT_POWER_WATTS", "123.4")
    metrics = run_near_term_trial(
        kernel_metrics={
            "pruning_ratio": 0.20,
            "tokens_pruned": 103,
            "complexity_overhead": 0.02,
        },
        experiment_id="exp_002_token_pruning",
        benchmark_id="transformer_inference_small",
        trial_num=2,
        baseline=BASELINE,
    )

    assert metrics["energy_telemetry_mode"] == "direct"
    assert metrics["metric_sources"]["power_watts"] == "direct"
    assert metrics["power_sample_count"] >= 1