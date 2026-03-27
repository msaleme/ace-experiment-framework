"""Single verdict engine with explicit gate traces and split-aware checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List
import statistics

from src.model import ExperimentRecord, MetricSet, Verdict
from src.stats_evaluator import StatsEvaluator


@dataclass
class GateResult:
    gate: str
    passed: bool
    evidence: Dict[str, Any]


class DecisionEngine:
    """Evaluates all configured constraints and emits one structured verdict trace."""

    ENGINE_VERSION = "single_decision_engine_v1"

    def evaluate(
        self,
        experiment: ExperimentRecord,
        trials: List[MetricSet],
        stats_evaluator: StatsEvaluator,
    ) -> Dict[str, Any]:
        configured = self._configured_constraints(experiment)
        split_scores = {
            split: self._score_split(trials, split, stats_evaluator, experiment)
            for split in ("development", "validation", "holdout")
        }

        checked_constraints: List[str] = []
        gates: List[GateResult] = []

        def add_gate(gate: str, passed: bool, evidence: Dict[str, Any]) -> None:
            gates.append(GateResult(gate=gate, passed=passed, evidence=evidence))

        min_ecd = float(configured.get("minimum_ecd_improvement", configured.get("minimum_effect_size", 0.0)))
        checked_constraints.append("minimum_ecd_improvement")
        add_gate(
            "development_minimum_ecd",
            split_scores["development"]["has_data"] and split_scores["development"]["ecd_mean"] >= min_ecd,
            {
                "required": min_ecd,
                "actual": split_scores["development"]["ecd_mean"],
                "has_data": split_scores["development"]["has_data"],
            },
        )

        min_effect = float(configured.get("minimum_effect_size", min_ecd))
        checked_constraints.append("minimum_effect_size")
        add_gate(
            "development_minimum_effect",
            split_scores["development"]["has_data"] and abs(split_scores["development"]["effect_size"]) >= min_effect,
            {
                "required": min_effect,
                "actual": split_scores["development"]["effect_size"],
                "has_data": split_scores["development"]["has_data"],
            },
        )

        require_significance = bool(configured.get("require_statistical_significance", True))
        checked_constraints.append("require_statistical_significance")
        add_gate(
            "development_significance",
            (not require_significance)
            or (split_scores["development"]["has_data"] and split_scores["development"]["significant"]),
            {
                "required": require_significance,
                "actual": split_scores["development"]["significant"],
                "p_value": split_scores["development"]["p_value"],
            },
        )

        require_ci_ex0 = bool(configured.get("confidence_interval_excludes_zero", True))
        checked_constraints.append("confidence_interval_excludes_zero")
        add_gate(
            "development_confidence_interval",
            (not require_ci_ex0)
            or (split_scores["development"]["has_data"] and split_scores["development"]["ci_excludes_zero"]),
            {
                "required": require_ci_ex0,
                "actual": split_scores["development"]["ci_excludes_zero"],
                "ci": split_scores["development"]["confidence_interval"],
            },
        )

        quality_floor_relative = float(configured.get("quality_floor_relative", experiment.evaluation_config.quality_floor))
        baseline_quality = float(
            experiment.raw_results.get("baseline_metrics", {}).get("accuracy", 0.9847)
        )
        quality_floor = (
            baseline_quality * quality_floor_relative
            if quality_floor_relative <= 1.5
            else quality_floor_relative
        )
        checked_constraints.append("quality_floor_relative")
        add_gate(
            "development_quality_floor",
            split_scores["development"]["has_data"] and split_scores["development"]["quality_mean"] >= quality_floor,
            {
                "required": quality_floor,
                "quality_floor_relative": quality_floor_relative,
                "baseline_quality": baseline_quality,
                "actual": split_scores["development"]["quality_mean"],
                "has_data": split_scores["development"]["has_data"],
            },
        )

        configured_confidence = float(configured.get("confidence_level", experiment.evaluation_config.confidence_level))
        checked_constraints.append("confidence_level")
        add_gate(
            "confidence_level_configured",
            abs(configured_confidence - experiment.evaluation_config.confidence_level) < 1e-9,
            {
                "configured": configured_confidence,
                "used": experiment.evaluation_config.confidence_level,
            },
        )

        require_validation_transfer = bool(configured.get("require_validation_transfer", False))
        checked_constraints.append("require_validation_transfer")
        add_gate(
            "validation_transfer",
            (not require_validation_transfer)
            or (
                split_scores["validation"]["has_data"]
                and split_scores["validation"]["ecd_mean"] >= min_ecd
                and split_scores["validation"]["quality_mean"] >= quality_floor
            ),
            {
                "required": require_validation_transfer,
                "validation_has_data": split_scores["validation"]["has_data"],
                "validation_ecd": split_scores["validation"]["ecd_mean"],
                "validation_quality": split_scores["validation"]["quality_mean"],
                "minimum_ecd_required": min_ecd,
                "quality_floor_required": quality_floor,
            },
        )

        require_holdout = bool(configured.get("require_holdout_pass", experiment.evaluation_config.require_holdout_pass))
        checked_constraints.append("require_holdout_pass")
        add_gate(
            "holdout_independent_gate",
            (not require_holdout)
            or (
                split_scores["holdout"]["has_data"]
                and split_scores["holdout"]["ecd_mean"] >= min_ecd
                and split_scores["holdout"]["quality_mean"] >= quality_floor
            ),
            {
                "required": require_holdout,
                "holdout_has_data": split_scores["holdout"]["has_data"],
                "holdout_ecd": split_scores["holdout"]["ecd_mean"],
                "holdout_quality": split_scores["holdout"]["quality_mean"],
                "minimum_ecd_required": min_ecd,
                "quality_floor_required": quality_floor,
            },
        )

        max_complexity_overhead = configured.get("maximum_complexity_overhead")
        if max_complexity_overhead is not None:
            max_complexity_overhead = float(max_complexity_overhead)
        else:
            max_complexity_overhead = float("inf")
        checked_constraints.append("maximum_complexity_overhead")
        complexity_actual = split_scores["development"]["complexity_overhead_mean"]
        complexity_data_present = split_scores["development"]["complexity_overhead_samples"] > 0
        add_gate(
            "complexity_overhead_gate",
            complexity_data_present and complexity_actual <= max_complexity_overhead,
            {
                "required": max_complexity_overhead,
                "actual": complexity_actual,
                "samples": split_scores["development"]["complexity_overhead_samples"],
            },
        )

        configured_keys = sorted(k for k in configured.keys())
        uncovered = [
            key for key in configured_keys if key not in checked_constraints
        ]
        add_gate(
            "configured_constraint_coverage",
            len(uncovered) == 0,
            {
                "configured": configured_keys,
                "checked": sorted(set(checked_constraints)),
                "uncovered": uncovered,
            },
        )

        all_passed = all(g.passed for g in gates)
        verdict = Verdict.ACCEPTED if all_passed else Verdict.REJECTED

        trace = {
            "engine_version": self.ENGINE_VERSION,
            "engine_only_verdict": True,
            "configured_constraints": configured,
            "split_scores": split_scores,
            "gates": [
                {"gate": g.gate, "passed": g.passed, "evidence": g.evidence}
                for g in gates
            ],
            "constraint_coverage": {
                "configured": configured_keys,
                "checked": sorted(set(checked_constraints)),
                "uncovered": uncovered,
                "all_checked": len(uncovered) == 0,
            },
            "final_verdict": verdict.value,
        }

        return {"verdict": verdict, "trace": trace}

    def _configured_constraints(self, experiment: ExperimentRecord) -> Dict[str, Any]:
        cfg = experiment.raw_results.get("configured_constraints", {}) if experiment.raw_results else {}
        acceptance = dict(cfg.get("acceptance", {}))
        quality_cfg = cfg.get("quality_floor", {})
        if "quality_floor_relative" not in acceptance:
            acceptance["quality_floor_relative"] = quality_cfg.get(
                "minimum_relative_to_baseline",
                experiment.evaluation_config.quality_floor,
            )
        return acceptance

    @staticmethod
    def _score_split(
        trials: Iterable[MetricSet],
        split: str,
        stats_evaluator: StatsEvaluator,
        experiment: ExperimentRecord,
    ) -> Dict[str, Any]:
        split_trials = [t for t in trials if getattr(t, "split", "") == split and t.success]
        ecd_values = [DecisionEngine._as_float(t.metrics.get("ecd_improvement")) for t in split_trials if "ecd_improvement" in t.metrics]
        quality_values = [DecisionEngine._as_float(t.metrics.get("accuracy")) for t in split_trials if "accuracy" in t.metrics]
        latency_values = [DecisionEngine._as_float(t.metrics.get("latency_ms")) for t in split_trials if "latency_ms" in t.metrics]
        energy_values = [DecisionEngine._as_float(t.metrics.get("energy_joules")) for t in split_trials if "energy_joules" in t.metrics]
        runtime_values = [DecisionEngine._as_float(t.metrics.get("runtime_ms")) for t in split_trials if "runtime_ms" in t.metrics]
        throughput_values = [DecisionEngine._as_float(t.metrics.get("throughput_tok_sec")) for t in split_trials if "throughput_tok_sec" in t.metrics]
        memory_values = [DecisionEngine._as_float(t.metrics.get("memory_peak_mb")) for t in split_trials if "memory_peak_mb" in t.metrics]
        complexity_values = [DecisionEngine._as_float(t.metrics.get("complexity_overhead")) for t in split_trials if "complexity_overhead" in t.metrics]

        if len(ecd_values) >= 2:
            baseline = [0.0] * len(ecd_values)
            effect_size = stats_evaluator.compute_effect_size(ecd_values, baseline)
            ci = stats_evaluator.compute_confidence_interval(
                ecd_values,
                confidence_level=experiment.evaluation_config.confidence_level,
            )
            ttest = stats_evaluator.perform_welch_ttest(ecd_values, baseline)
            significant = bool(ttest["significant"])
            p_value = float(ttest["p_value"])
            ci_excludes_zero = bool((ci[0] > 0) or (ci[1] < 0))
        else:
            effect_size = 0.0
            ci = (0.0, 0.0)
            significant = False
            p_value = 1.0
            ci_excludes_zero = False

        sources = {"direct": 0, "estimated": 0, "derived": 0, "benchmark-scored": 0, "unknown": 0}
        for trial in split_trials:
            for source in getattr(trial, "metric_sources", {}).values():
                if source in sources:
                    sources[source] += 1
                else:
                    sources["unknown"] += 1

        return {
            "has_data": len(split_trials) > 0,
            "trials": len(split_trials),
            "ecd_mean": DecisionEngine._mean_or_default(ecd_values, 0.0),
            "quality_mean": DecisionEngine._mean_or_default(quality_values, 0.0),
            "latency_p95": DecisionEngine._p95_or_default(latency_values, 0.0),
            "energy_mean": DecisionEngine._mean_or_default(energy_values, 0.0),
            "runtime_mean_ms": DecisionEngine._mean_or_default(runtime_values, 0.0),
            "throughput_mean": DecisionEngine._mean_or_default(throughput_values, 0.0),
            "memory_peak_mean_mb": DecisionEngine._mean_or_default(memory_values, 0.0),
            "complexity_overhead_mean": DecisionEngine._mean_or_default(complexity_values, 0.0),
            "complexity_overhead_samples": len(complexity_values),
            "effect_size": effect_size,
            "confidence_interval": [float(ci[0]), float(ci[1])],
            "ci_excludes_zero": ci_excludes_zero,
            "significant": significant,
            "p_value": p_value,
            "metric_source_counts": sources,
        }

    @staticmethod
    def _as_float(value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _mean_or_default(values: List[float], default: float) -> float:
        if not values:
            return default
        return float(statistics.mean(values))

    @staticmethod
    def _p95_or_default(values: List[float], default: float) -> float:
        if not values:
            return default
        ordered = sorted(values)
        idx = int(round(0.95 * (len(ordered) - 1)))
        return float(ordered[idx])