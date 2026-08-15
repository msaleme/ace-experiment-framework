"""Archivist agent: persist outcomes and generate reports."""

from __future__ import annotations

from typing import Dict, Any

from ace_lab.results_store import ResultsStore
from ace_lab.report_generator import ReportGenerator
from ace_lab.model import ExperimentRecord


class ArchivistAgent:
    def archive(self, store: ResultsStore, report_generator: ReportGenerator, experiment: ExperimentRecord) -> Dict[str, Any]:
        exp_path = store.save_experiment(experiment)
        report_path = report_generator.generate_experiment_report(experiment)
        return {"experiment_path": str(exp_path), "report_path": str(report_path)}
