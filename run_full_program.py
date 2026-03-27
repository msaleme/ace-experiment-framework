#!/usr/bin/env python3
"""Full ACE program runner across near-term, mid-term, and moonshot lanes."""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Set

from src.model import (
    HorizonCategory,
    WorkloadClass,
    EvaluationConfig,
    Verdict,
)
from src.baseline_manager import BaselineManager
from src.benchmark_registry import BenchmarkRegistry
from src.metrics_collector import MetricsCollector
from src.experiment_runner import ExperimentRunner
from src.stats_evaluator import StatsEvaluator
from src.results_store import ResultsStore
from src.report_generator import ReportGenerator

from agents.hypothesis.hypothesis_agent import HypothesisAgent
from agents.build.build_agent import BuildAgent
from agents.eval.evaluation_agent import EvaluationAgent
from agents.stats.statistics_agent import StatisticsAgent
from agents.skeptic.skeptic_agent import SkepticAgent
from agents.archivist.archivist_agent import ArchivistAgent

from harness.runners.config_loader import ensure_baseline_from_yaml, ensure_benchmark_from_yaml
from harness.validation.portfolio_intelligence import PortfolioIntelligence


def _json_safe(value):
    """Convert numpy/scipy scalar objects to builtin Python types."""
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            return value
    return value


def _map_horizon(value: str) -> HorizonCategory:
    if value == "near_term":
        return HorizonCategory.NEAR_TERM
    if value == "mid_term":
        return HorizonCategory.MID_TERM
    return HorizonCategory.MOONSHOT


def _map_workload(experiment_id: str) -> WorkloadClass:
    if "token" in experiment_id:
        return WorkloadClass.SPARSE_CONDITIONAL
    if "memory" in experiment_id:
        return WorkloadClass.MEMORY_BOUND
    if "compiler" in experiment_id:
        return WorkloadClass.DENSE_LINEAR_ALGEBRA
    if "analog" in experiment_id:
        return WorkloadClass.END_TO_END
    return WorkloadClass.DENSE_LINEAR_ALGEBRA


def _map_workload_from_value(value: str, fallback_experiment_id: str) -> WorkloadClass:
    try:
        return WorkloadClass(value)
    except Exception:
        return _map_workload(fallback_experiment_id)


def _load_top5_ids(report_path: Path) -> Set[str]:
    if not report_path.exists():
        raise FileNotFoundError(f"Top-5 report not found: {report_path}")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    return {item["experiment_id"] for item in report.get("top5_credible_wins", [])}


def run_full_program(root: Path, selected_experiment_ids: Optional[Set[str]] = None) -> int:
    print("=" * 90)
    print("ACE FULL PROGRAM EXECUTION")
    print("=" * 90)

    baselines_dir = root / "baselines"
    benchmarks_dir = root / "configs" / "benchmarks"
    results_dir = root / "results"
    reports_dir = root / "reports"

    baseline_manager = BaselineManager(baselines_dir)
    benchmark_registry = BenchmarkRegistry(benchmarks_dir)
    metrics_collector = MetricsCollector(results_dir)
    stats_evaluator = StatsEvaluator(metrics_collector)
    results_store = ResultsStore(results_dir)
    report_generator = ReportGenerator(reports_dir)

    # Ensure baseline and benchmarks loaded into immutable registry stores.
    baseline_id = ensure_baseline_from_yaml(
        baseline_manager, root / "baselines" / "baseline_gpu_transformer_bf16_v1.yaml"
    )
    for benchmark_file in sorted((root / "configs" / "benchmarks").glob("*.yaml")):
        ensure_benchmark_from_yaml(benchmark_registry, benchmark_file)

    # Agents
    hypothesis_agent = HypothesisAgent()
    build_agent = BuildAgent()
    eval_agent = EvaluationAgent()
    statistics_agent = StatisticsAgent()
    skeptic_agent = SkepticAgent()
    archivist_agent = ArchivistAgent()

    proposals = hypothesis_agent.dedupe(
        hypothesis_agent.propose(baseline_id, root / "experiments")
    )

    if selected_experiment_ids:
        proposals = [p for p in proposals if p.experiment_id in selected_experiment_ids]

    print(f"Proposals: {len(proposals)}")

    executed = []
    for proposal in proposals:
        print("-" * 90)
        print(f"Running {proposal.experiment_id} ({proposal.horizon})")

        runner = ExperimentRunner(
            baseline_manager=baseline_manager,
            benchmark_registry=benchmark_registry,
            metrics_collector=metrics_collector,
            experiments_dir=root / "experiments" / proposal.horizon,
        )

        exp = runner.create_experiment(
            experiment_id=proposal.experiment_id,
            hypothesis_text=proposal.hypothesis_text,
            horizon_category=_map_horizon(proposal.horizon),
            workload_class=_map_workload_from_value(proposal.workload_class, proposal.experiment_id),
            hardware_target="A100",
            representation_type=proposal.representation_type,
            mutation_scope=proposal.mutation_scope,
            baseline_reference=proposal.baseline_reference,
            benchmark_set=proposal.benchmark_set,
            evaluation_config=EvaluationConfig(
                quality_floor=proposal.quality_floor,
                latency_budget_ms_p95=120.0,
                minimum_effect_threshold=float(
                    proposal.acceptance.get("minimum_effect_size", proposal.acceptance.get("minimum_ecd_improvement", 0.10))
                ),
                trials=proposal.trials,
                confidence_level=float(proposal.acceptance.get("confidence_level", 0.95)),
                require_holdout_pass=bool(proposal.acceptance.get("require_holdout_pass", True)),
            ),
            notes="Auto-generated by full ACE closed-loop runner",
        )

        exp.raw_results["benchmark_sets"] = proposal.benchmark_sets
        exp.raw_results["configured_constraints"] = {
            "acceptance": proposal.acceptance,
            "quality_floor": proposal.quality_floor_config,
        }
        exp.raw_results["reporting"] = proposal.reporting
        exp.raw_results["maturity_label"] = proposal.maturity_label
        exp.raw_results["metric_types"] = {
            "near_term": "direct+estimated",
            "mid_term": "estimated",
            "moonshot": "estimated",
        }
        baseline_snapshot = baseline_manager.get_baseline(proposal.baseline_reference)
        baseline_measurements = {}
        if baseline_snapshot:
            baseline_measurements = baseline_snapshot.hardware.metadata.get("baseline_measurements", {})
        exp.raw_results["baseline_metrics"] = baseline_measurements

        trial_executor = build_agent.build_trial_executor(proposal.experiment_id)
        exp = eval_agent.execute(runner, exp.experiment_id, trial_executor)

        trial_sets = metrics_collector.get_all_trials(exp.experiment_id)
        decision = statistics_agent.evaluate(stats_evaluator, exp, trial_sets)
        exp.statistical_assessment = _json_safe(decision["trace"])
        exp.verdict = decision["verdict"]
        exp.raw_results["decision_trace"] = _json_safe(decision["trace"])
        exp.raw_results["verdict_source"] = decision["trace"].get("engine_version", "unknown")

        summary = metrics_collector.get_summarized_results(exp.experiment_id)
        exp.summarized_results = summary

        skeptic = skeptic_agent.review(exp, summary)
        if skeptic["suspicious"] and exp.verdict == Verdict.ACCEPTED:
            exp.verdict = Verdict.PROMISING_BUT_COMPLEX

        exp.notes = (
            (exp.notes or "")
            + "\nSkeptic review: "
            + " | ".join(skeptic["notes"])
        )

        artifacts = archivist_agent.archive(results_store, report_generator, exp)
        executed.append(exp)

        print(f"Verdict: {exp.verdict.value}")
        print(f"Artifacts: {artifacts['experiment_path']} | {artifacts['report_path']}")

    dashboard_path = report_generator.generate_portfolio_dashboard(executed)
    ranking = PortfolioIntelligence().rank(executed)

    ranking_path = reports_dir / "portfolio_ranking.json"
    ranking_path.write_text(json.dumps(ranking, indent=2), encoding="utf-8")

    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "executed": len(executed),
        "accepted": sum(1 for e in executed if e.verdict == Verdict.ACCEPTED),
        "rejected": sum(1 for e in executed if e.verdict == Verdict.REJECTED),
        "promising_but_complex": sum(1 for e in executed if e.verdict == Verdict.PROMISING_BUT_COMPLEX),
        "dashboard": str(dashboard_path),
        "ranking": str(ranking_path),
    }

    summary_path = reports_dir / "full_program_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=" * 90)
    print("FULL PROGRAM COMPLETE")
    print(json.dumps(summary, indent=2))
    print("=" * 90)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ACE full program")
    parser.add_argument(
        "--experiment-id",
        action="append",
        dest="experiment_ids",
        help="Run only specific experiment IDs (repeatable)",
    )
    parser.add_argument(
        "--top5-credible",
        action="store_true",
        help="Run only top-5 credible wins from reports/verification_pack.json",
    )
    parser.add_argument(
        "--top5-report",
        default="reports/verification_pack.json",
        help="Path to verification pack JSON with top5_credible_wins",
    )

    args = parser.parse_args()

    selected_ids = set(args.experiment_ids or [])
    if args.top5_credible:
        selected_ids.update(
            _load_top5_ids(Path(__file__).resolve().parent / args.top5_report)
        )

    raise SystemExit(
        run_full_program(
            Path(__file__).resolve().parent,
            selected_experiment_ids=selected_ids or None,
        )
    )
