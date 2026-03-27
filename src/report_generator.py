"""
Report Generator: creates markdown and HTML reports for experiments.
Generates experiment records, comparison reports, and portfolio dashboards.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.model import ExperimentRecord, Verdict


class ReportGenerator:
    """
    Generate reports for experiments and portfolios.
    
    Produces:
    1. Individual experiment reports
    2. Comparison cohort reports
    3. Portfolio dashboards
    4. Trend analyses
    """
    
    def __init__(self, reports_dir: Path = Path("reports")):
        """Initialize report generator."""
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_experiment_report(
        self,
        experiment: ExperimentRecord,
        include_raw_data: bool = True,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Generate a markdown report for a single experiment.
        
        Args:
            experiment: ExperimentRecord to report
            include_raw_data: If True, include raw metrics
            output_path: Optional custom output path
            
        Returns:
            Path where report was written
        """
        if output_path is None:
            output_path = self.reports_dir / f"{experiment.experiment_id}_report.md"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build report content
        content = self._build_experiment_report_content(experiment, include_raw_data)
        
        output_path.write_text(content)
        return output_path
    
    def generate_comparison_report(
        self,
        experiments: List[ExperimentRecord],
        title: str = "Experiment Comparison",
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Generate a comparison report across multiple experiments.
        
        Args:
            experiments: List of experiments to compare
            title: Report title
            output_path: Optional custom output path
            
        Returns:
            Path where report was written
        """
        if output_path is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            output_path = self.reports_dir / f"comparison_{timestamp}.md"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = self._build_comparison_report_content(experiments, title)
        
        output_path.write_text(content)
        return output_path
    
    def generate_portfolio_dashboard(
        self,
        experiments: List[ExperimentRecord],
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Generate a portfolio dashboard summarizing all experiments.
        
        Args:
            experiments: All experiments in portfolio
            output_path: Optional custom output path
            
        Returns:
            Path where dashboard was written
        """
        if output_path is None:
            output_path = self.reports_dir / "portfolio_dashboard.md"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = self._build_portfolio_dashboard_content(experiments)
        
        output_path.write_text(content)
        return output_path
    
    def _build_experiment_report_content(
        self,
        experiment: ExperimentRecord,
        include_raw_data: bool,
    ) -> str:
        """Build markdown content for experiment report."""
        lines = [
            f"# Experiment Report: {experiment.experiment_id}",
            "",
            "## Metadata",
            "",
            f"- **Hypothesis**: {experiment.hypothesis_text}",
            f"- **Horizon**: {experiment.horizon_category.value}",
            f"- **Workload Class**: {experiment.workload_class.value}",
            f"- **Hardware Target**: {experiment.hardware_target}",
            f"- **Representation Type**: {experiment.representation_type}",
            f"- **Parent Experiment**: {experiment.parent_experiment_id or 'None'}",
            f"- **Maturity Label**: {experiment.raw_results.get('maturity_label', 'unknown')}",
            f"- **Verdict Source**: {experiment.raw_results.get('verdict_source', 'unknown')}",
            "",
            "## Mutation Scope",
            "",
            "Permitted changes:",
            "",
            *[f"- {item}" for item in experiment.mutation_scope],
            "",
            "## Baseline Reference",
            "",
            f"- **Baseline ID**: {experiment.baseline_reference}",
            "",
            "## Benchmarks",
            "",
            *[f"- {bm}" for bm in experiment.benchmark_set],
            "",
            "## Execution Timeline",
            "",
            f"- **Created**: {experiment.created_timestamp.isoformat()}",
            f"- **Started**: {experiment.started_timestamp.isoformat() if experiment.started_timestamp else 'Not started'}",
            f"- **Completed**: {experiment.completed_timestamp.isoformat() if experiment.completed_timestamp else 'Not completed'}",
            "",
            "## Evaluation Configuration",
            "",
        ]
        
        config = experiment.evaluation_config
        lines.extend([
            f"- **Quality Floor**: {config.quality_floor:.0%}",
            f"- **Latency Budget (p95)**: {config.latency_budget_ms_p95:.1f} ms",
            f"- **Latency Budget (p99)**: {config.latency_budget_ms_p99:.1f} ms",
            f"- **Minimum Effect Threshold**: {config.minimum_effect_threshold:.0%}",
            f"- **Number of Trials**: {config.trials}",
            f"- **Confidence Level**: {config.confidence_level:.0%}",
            f"- **Require Holdout Pass**: {config.require_holdout_pass}",
            "",
            "## Results Summary",
            "",
            f"- **Verdict**: {experiment.verdict.value.upper()}",
            "",
        ])
        
        if experiment.summarized_results:
            lines.extend([
                "### Summarized Metrics",
                "",
            ])
            
            for metric_name, stats in experiment.summarized_results.items():
                lines.extend([
                    f"#### {metric_name}",
                    "",
                    f"- Mean: {stats.get('mean', 'N/A')}",
                    f"- Std Dev: {stats.get('std', 'N/A')}",
                    f"- Min: {stats.get('min', 'N/A')}",
                    f"- Max: {stats.get('max', 'N/A')}",
                    f"- p95: {stats.get('p95', 'N/A')}",
                    f"- p99: {stats.get('p99', 'N/A')}",
                    "",
                ])
        
        if experiment.statistical_assessment:
            lines.extend([
                "### Statistical Assessment",
                "",
                "```json",
                json.dumps(experiment.statistical_assessment, indent=2),
                "```",
                "",
            ])
        
        if experiment.notes:
            lines.extend([
                "## Notes",
                "",
                experiment.notes,
                "",
            ])
        
        lines.extend([
            "## Reproducibility",
            "",
            f"- **Code Commit**: {experiment.code_commit_hash}",
            f"- **Artifact Paths**:",
            "",
        ])
        
        for key, path in experiment.artifact_paths.items():
            lines.append(f"  - {key}: {path}")
        
        return "\n".join(lines)
    
    def _build_comparison_report_content(
        self,
        experiments: List[ExperimentRecord],
        title: str,
    ) -> str:
        """Build markdown content for comparison report."""
        lines = [
            f"# {title}",
            "",
            f"Generated: {datetime.utcnow().isoformat()}",
            "",
            f"## Summary",
            "",
            f"- **Total Experiments**: {len(experiments)}",
            f"- **Accepted**: {sum(1 for e in experiments if e.verdict == Verdict.ACCEPTED)}",
            f"- **Rejected**: {sum(1 for e in experiments if e.verdict == Verdict.REJECTED)}",
            f"- **Inconclusive**: {sum(1 for e in experiments if e.verdict == Verdict.INCONCLUSIVE)}",
            "",
            "## Experiment Comparison Table",
            "",
            "| Experiment ID | Hypothesis | Horizon | Verdict | Effect Size |",
            "|---|---|---|---|---|",
        ]
        
        for exp in experiments:
            effect = "N/A"
            if exp.statistical_assessment and 'effect_size' in exp.statistical_assessment:
                effect = f"{exp.statistical_assessment['effect_size']:.3f}"
            
            hypothesis_short = (exp.hypothesis_text[:50] + "...") if len(exp.hypothesis_text) > 50 else exp.hypothesis_text
            
            lines.append(
                f"| {exp.experiment_id} | {hypothesis_short} | {exp.horizon_category.value} | {exp.verdict.value} | {effect} |"
            )
        
        lines.extend([
            "",
            "## Detailed Results",
            "",
        ])
        
        # Group by verdict
        by_verdict = {}
        for exp in experiments:
            v = exp.verdict.value
            if v not in by_verdict:
                by_verdict[v] = []
            by_verdict[v].append(exp)
        
        for verdict_str in sorted(by_verdict.keys()):
            exps = by_verdict[verdict_str]
            lines.extend([
                f"### {verdict_str.upper()} ({len(exps)})",
                "",
            ])
            
            for exp in exps:
                lines.extend([
                    f"#### {exp.experiment_id}",
                    "",
                    f"- Hypothesis: {exp.hypothesis_text}",
                    f"- Hardware: {exp.hardware_target}",
                    f"- Benchmarks: {', '.join(exp.benchmark_set)}",
                    "",
                ])
        
        return "\n".join(lines)
    
    def _build_portfolio_dashboard_content(
        self,
        experiments: List[ExperimentRecord],
    ) -> str:
        """Build markdown content for portfolio dashboard."""
        lines = [
            "# ACE Lab - Portfolio Dashboard",
            "",
            f"Last Updated: {datetime.utcnow().isoformat()}",
            "",
            "## Portfolio Overview",
            "",
        ]
        
        # Statistics
        total = len(experiments)
        accepted = sum(1 for e in experiments if e.verdict == Verdict.ACCEPTED)
        rejected = sum(1 for e in experiments if e.verdict == Verdict.REJECTED)
        inconclusive = sum(1 for e in experiments if e.verdict == Verdict.INCONCLUSIVE)
        pending = sum(1 for e in experiments if e.verdict == Verdict.PENDING)
        
        lines.extend([
            f"- **Total Experiments**: {total}",
            f"- **Accepted**: {accepted} ({100*accepted//total if total else 0}%)",
            f"- **Rejected**: {rejected} ({100*rejected//total if total else 0}%)",
            f"- **Inconclusive**: {inconclusive} ({100*inconclusive//total if total else 0}%)",
            f"- **Pending**: {pending} ({100*pending//total if total else 0}%)",
            "",
            "## By Horizon",
            "",
        ])
        
        # Group by horizon
        horizons = {}
        for exp in experiments:
            h = exp.horizon_category.value
            if h not in horizons:
                horizons[h] = []
            horizons[h].append(exp)
        
        for horizon in sorted(horizons.keys()):
            exps = horizons[horizon]
            accepted_h = sum(1 for e in exps if e.verdict == Verdict.ACCEPTED)
            lines.extend([
                f"### {horizon.upper()}",
                f"- **Count**: {len(exps)}",
                f"- **Accepted**: {accepted_h}",
                "",
            ])
        
        lines.extend([
            "## Recent Experiments",
            "",
        ])
        
        # Sort by creation time
        recent = sorted(experiments, key=lambda e: e.created_timestamp, reverse=True)[:10]
        
        for exp in recent:
            lines.append(
                f"- [{exp.experiment_id}]({exp.experiment_id}_report.md): {exp.hypothesis_text[:60]}"
            )
        
        return "\n".join(lines)
