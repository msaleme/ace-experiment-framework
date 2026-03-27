"""Hypothesis agent: proposes and prioritizes experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import yaml


@dataclass
class ExperimentProposal:
    experiment_id: str
    horizon: str
    hypothesis_text: str
    workload_class: str
    mutation_scope: List[str]
    baseline_reference: str
    benchmark_set: List[str]
    representation_type: str
    quality_floor: float
    trials: int
    benchmark_sets: Dict[str, List[str]]
    acceptance: Dict[str, Any]
    quality_floor_config: Dict[str, Any]
    reporting: Dict[str, Any]
    maturity_label: str


class HypothesisAgent:
    def propose(self, baseline_id: str, experiments_root: Path) -> List[ExperimentProposal]:
        proposals: List[ExperimentProposal] = []

        for horizon in ("near_term", "mid_term", "moonshot"):
            lane_dir = experiments_root / horizon
            if not lane_dir.exists():
                continue

            for yaml_path in sorted(lane_dir.glob("*.yaml")):
                with yaml_path.open("r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)

                baseline_cfg = cfg.get("baseline", baseline_id)
                if isinstance(baseline_cfg, dict):
                    baseline_ref = baseline_cfg.get("baseline_id", baseline_id)
                else:
                    baseline_ref = str(baseline_cfg)

                bm_sets = cfg.get("benchmark_sets", {})
                benchmark_set = (
                    bm_sets.get("development", [])
                    + bm_sets.get("validation", [])
                    + bm_sets.get("holdout", [])
                )
                if not benchmark_set:
                    benchmark_set = [
                        "transformer_inference_small",
                        "transformer_inference_medium",
                        "transformer_inference_holdout",
                    ]

                qf = cfg.get("quality_floor", {}).get("minimum_relative_to_baseline", 0.99)
                trials = int(cfg.get("trials", 10))
                acceptance = cfg.get("acceptance", {})
                reporting = cfg.get("reporting", {})
                quality_floor_cfg = cfg.get("quality_floor", {})

                proposals.append(
                    ExperimentProposal(
                        experiment_id=cfg["experiment_id"],
                        horizon=cfg.get("horizon", horizon),
                        hypothesis_text=cfg.get("hypothesis", ""),
                        workload_class=cfg.get("workload_class", "dense_linear_algebra"),
                        mutation_scope=list(cfg.get("mutation_scope", [])),
                        baseline_reference=baseline_ref,
                        benchmark_set=benchmark_set,
                        representation_type=cfg.get("representation_type", "unspecified"),
                        quality_floor=float(qf),
                        trials=trials,
                        benchmark_sets={
                            "development": list(bm_sets.get("development", [])),
                            "validation": list(bm_sets.get("validation", [])),
                            "holdout": list(bm_sets.get("holdout", [])),
                        },
                        acceptance=dict(acceptance),
                        quality_floor_config=dict(quality_floor_cfg),
                        reporting=dict(reporting),
                        maturity_label=self._maturity_label(cfg.get("horizon", horizon)),
                    )
                )

        return proposals

    def dedupe(self, proposals: List[ExperimentProposal]) -> List[ExperimentProposal]:
        seen = set()
        out: List[ExperimentProposal] = []
        for p in proposals:
            if p.experiment_id in seen:
                continue
            out.append(p)
            seen.add(p.experiment_id)
        return out

    @staticmethod
    def _maturity_label(horizon: str) -> str:
        if horizon == "near_term":
            return "M5"
        if horizon == "mid_term":
            return "M3"
        return "M2"
