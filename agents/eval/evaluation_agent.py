"""Evaluation agent: executes repeated trials inside fixed harness."""

from __future__ import annotations

from typing import Callable

from ace_lab.experiment_runner import ExperimentRunner
from ace_lab.model import ExperimentRecord


class EvaluationAgent:
    def execute(self, runner: ExperimentRunner, experiment_id: str, trial_executor: Callable[[int, str], dict]) -> ExperimentRecord:
        return runner.run_experiment(experiment_id=experiment_id, trial_executor=trial_executor, dry_run=False)
