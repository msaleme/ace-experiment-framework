"""Cross-lane ranking and portfolio selection logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from src.model import ExperimentRecord, Verdict


@dataclass
class PortfolioWeights:
    ecd_gain: float = 0.35
    quality_preservation: float = 0.20
    robustness: float = 0.15
    latency_compliance: float = 0.10
    transferability: float = 0.10
    complexity_penalty: float = -0.10


class PortfolioIntelligence:
    """Compute portfolio score and suggest branching order."""

    def __init__(self, weights: PortfolioWeights | None = None):
        self.weights = weights or PortfolioWeights()

    def score_experiment(self, exp: ExperimentRecord) -> float:
        # Defaults keep scoring stable even when specific metrics are missing.
        summary = exp.summarized_results
        ecd_gain = float(summary.get("ecd_improvement", {}).get("mean", 0.0) or 0.0)

        quality = float(summary.get("accuracy", {}).get("mean", 0.0) or 0.0)
        quality_preservation = min(max(quality, 0.0), 1.0)

        std = float(summary.get("ecd_improvement", {}).get("std", 0.0) or 0.0)
        robustness = max(0.0, 1.0 - std)

        p95 = float(summary.get("latency_ms", {}).get("p95", 0.0) or 0.0)
        budget = exp.evaluation_config.latency_budget_ms_p95 or 1.0
        latency_compliance = 1.0 if p95 <= budget else max(0.0, 1.0 - (p95 - budget) / budget)

        transferability = 1.0 if exp.verdict == Verdict.ACCEPTED else 0.5
        complexity = 0.03

        score = (
            self.weights.ecd_gain * ecd_gain
            + self.weights.quality_preservation * quality_preservation
            + self.weights.robustness * robustness
            + self.weights.latency_compliance * latency_compliance
            + self.weights.transferability * transferability
            + self.weights.complexity_penalty * complexity
        )
        return float(score)

    def rank(self, experiments: List[ExperimentRecord]) -> List[Dict[str, float | str]]:
        ranked = [
            {"experiment_id": exp.experiment_id, "score": self.score_experiment(exp), "verdict": exp.verdict.value}
            for exp in experiments
        ]
        ranked.sort(key=lambda x: float(x["score"]), reverse=True)
        return ranked
