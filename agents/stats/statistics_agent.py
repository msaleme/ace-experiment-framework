"""Statistics agent: delegates verdict generation to the single decision engine."""

from __future__ import annotations

from typing import Dict, Any, List

from src.decision_engine import DecisionEngine
from src.stats_evaluator import StatsEvaluator
from src.model import ExperimentRecord, MetricSet


class StatisticsAgent:
    def __init__(self):
        self.engine = DecisionEngine()

    def evaluate(
        self,
        stats_evaluator: StatsEvaluator,
        experiment: ExperimentRecord,
        trial_sets: List[MetricSet],
    ) -> Dict[str, Any]:
        return self.engine.evaluate(
            experiment=experiment,
            trials=trial_sets,
            stats_evaluator=stats_evaluator,
        )
