from src.decision_engine import DecisionEngine
from src.model import EvaluationConfig, ExperimentRecord, HorizonCategory, MetricSet, Verdict, WorkloadClass
from src.metrics_collector import MetricsCollector
from src.stats_evaluator import StatsEvaluator
from agents.stats.statistics_agent import StatisticsAgent


def _build_experiment(require_holdout: bool = True) -> ExperimentRecord:
    exp = ExperimentRecord(
        experiment_id="hardening_test_exp",
        hypothesis_text="test",
        horizon_category=HorizonCategory.NEAR_TERM,
        workload_class=WorkloadClass.DENSE_LINEAR_ALGEBRA,
        baseline_reference="baseline_gpu_transformer_bf16_v1",
        benchmark_set=["transformer_inference_small", "transformer_inference_medium"],
        evaluation_config=EvaluationConfig(
            quality_floor=0.95,
            minimum_effect_threshold=0.1,
            trials=3,
            confidence_level=0.95,
            require_holdout_pass=require_holdout,
        ),
    )
    exp.raw_results = {
        "configured_constraints": {
            "acceptance": {
                "minimum_ecd_improvement": 0.1,
                "minimum_effect_size": 0.1,
                "require_statistical_significance": True,
                "confidence_interval_excludes_zero": True,
                "require_holdout_pass": require_holdout,
                "require_validation_transfer": True,
                "maximum_complexity_overhead": 0.05,
            },
            "quality_floor": {
                "minimum_relative_to_baseline": 0.95,
            },
        }
    }
    return exp


def _make_trial(trial_num: int, split: str, ecd: float, quality: float, complexity: float = 0.02) -> MetricSet:
    return MetricSet(
        trial_num=trial_num,
        split=split,
        benchmark_id=f"{split}_benchmark",
        metrics={
            "ecd_improvement": ecd,
            "accuracy": quality,
            "latency_ms": 50.0,
            "energy_joules": 0.2,
            "runtime_ms": 50.0,
            "throughput_tok_sec": 20.0,
            "memory_peak_mb": 120.0,
            "complexity_overhead": complexity,
        },
        metric_sources={
            "latency_ms": "direct",
            "runtime_ms": "direct",
            "throughput_tok_sec": "direct",
            "memory_peak_mb": "direct",
            "energy_joules": "estimated",
            "accuracy": "estimated",
            "ecd_improvement": "estimated",
            "complexity_overhead": "estimated",
        },
        success=True,
    )


def test_holdout_gate_fails_if_holdout_missing():
    exp = _build_experiment(require_holdout=True)
    collector = MetricsCollector()
    evaluator = StatsEvaluator(collector)
    engine = DecisionEngine()

    trials = [
        _make_trial(1, "development", 0.20, 0.97),
        _make_trial(2, "development", 0.19, 0.97),
        _make_trial(3, "validation", 0.17, 0.96),
        _make_trial(4, "validation", 0.18, 0.96),
    ]

    result = engine.evaluate(exp, trials, evaluator)
    holdout_gate = next(g for g in result["trace"]["gates"] if g["gate"] == "holdout_independent_gate")

    assert result["verdict"] == Verdict.REJECTED
    assert holdout_gate["passed"] is False
    assert holdout_gate["evidence"]["holdout_has_data"] is False


def test_verdicts_are_engine_stamped_and_covered():
    exp = _build_experiment(require_holdout=True)
    collector = MetricsCollector()
    evaluator = StatsEvaluator(collector)
    engine = DecisionEngine()

    trials = [
        _make_trial(1, "development", 0.20, 0.97),
        _make_trial(2, "development", 0.22, 0.97),
        _make_trial(3, "validation", 0.19, 0.96),
        _make_trial(4, "validation", 0.18, 0.96),
        _make_trial(5, "holdout", 0.16, 0.96),
        _make_trial(6, "holdout", 0.17, 0.96),
    ]

    result = engine.evaluate(exp, trials, evaluator)
    trace = result["trace"]

    assert trace["engine_version"] == DecisionEngine.ENGINE_VERSION
    assert trace["engine_only_verdict"] is True
    assert trace["constraint_coverage"]["all_checked"] is True
    assert trace["constraint_coverage"]["uncovered"] == []


def test_statistics_agent_uses_single_decision_engine():
    exp = _build_experiment(require_holdout=False)
    collector = MetricsCollector()
    evaluator = StatsEvaluator(collector)
    stats_agent = StatisticsAgent()

    trials = [
        _make_trial(1, "development", 0.20, 0.97),
        _make_trial(2, "development", 0.21, 0.97),
        _make_trial(3, "validation", 0.18, 0.96),
        _make_trial(4, "validation", 0.19, 0.96),
    ]

    result = stats_agent.evaluate(evaluator, exp, trials)
    assert result["trace"]["engine_version"] == DecisionEngine.ENGINE_VERSION