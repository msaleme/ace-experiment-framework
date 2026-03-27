"""Moonshot simulators for analog/photonic/in-memory concepts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import random


@dataclass
class MoonshotConfig:
    substrate: str
    projected_gain: float
    novelty_score: float


def run_moonshot_proxy(config: MoonshotConfig, seed: int) -> Dict[str, float]:
    random.seed(seed)
    noise_penalty = random.uniform(0.0, 0.4)
    projected_system_gain = max(0.0, config.projected_gain - noise_penalty)

    return {
        "accuracy": 0.93 + random.uniform(-0.03, 0.02),
        "latency_ms": 95.0 + random.uniform(-10.0, 10.0),
        "energy_joules": 0.42 + random.uniform(-0.07, 0.05),
        "throughput_tok_sec": 10.8 + random.uniform(-1.1, 1.0),
        "ecd_improvement": projected_system_gain,
        "system_level_ecd_projection": projected_system_gain,
        "novelty_score": config.novelty_score,
    }
