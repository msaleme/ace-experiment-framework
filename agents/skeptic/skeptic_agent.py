"""Skeptic agent: challenge suspicious wins and enforce holdout confirmation."""

from __future__ import annotations

from typing import Dict, Any

from src.model import ExperimentRecord


class SkepticAgent:
    OLD_RULE = "ecd.std > 0.20"
    NEW_RULE = "(ecd.std / max(abs(ecd.mean), eps)) + (ecd_uncertainty.mean / max(abs(ecd.mean), eps)) > 0.35"

    def review(self, experiment: ExperimentRecord, summary: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        notes = []
        suspicious = False

        ecd = summary.get("ecd_improvement", {})
        ecd_uncertainty = summary.get("ecd_improvement_uncertainty", {})

        mean_abs = abs(float(ecd.get("mean", 0.0)))
        eps = 1e-9
        normalized_std = float(ecd.get("std", 0.0)) / max(mean_abs, eps)
        normalized_uncertainty = float(ecd_uncertainty.get("mean", 0.0)) / max(mean_abs, eps)
        instability_score = normalized_std + normalized_uncertainty

        old_rule_triggered = bool(ecd and ecd.get("std", 0.0) and ecd["std"] > 0.20)
        new_rule_triggered = instability_score > 0.35

        if new_rule_triggered:
            suspicious = True
            notes.append(
                "Uncertainty-normalized instability in ECD exceeds threshold "
                f"(score={instability_score:.4f}, std_norm={normalized_std:.4f}, unc_norm={normalized_uncertainty:.4f})."
            )

        if experiment.benchmark_set and "transformer_inference_holdout" not in experiment.benchmark_set:
            suspicious = True
            notes.append("Missing holdout benchmark in declared benchmark_set.")

        if not notes:
            notes.append("No obvious benchmark leakage or instability detected.")

        return {
            "suspicious": suspicious,
            "notes": notes,
            "rule_debug": {
                "old_rule": self.OLD_RULE,
                "old_rule_triggered": old_rule_triggered,
                "new_rule": self.NEW_RULE,
                "new_rule_triggered": new_rule_triggered,
                "instability_score": instability_score,
                "normalized_std": normalized_std,
                "normalized_uncertainty": normalized_uncertainty,
            },
        }
