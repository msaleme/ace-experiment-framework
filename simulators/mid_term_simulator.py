"""Mid-term proxy simulators for alternative numeric representations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import random


@dataclass
class MidTermConfig:
    representation: str
    conversion_overhead: float
    base_ecd_gain: float


def run_mid_term_proxy(config: MidTermConfig, seed: int) -> Dict[str, float]:
    random.seed(seed)
    jitter = random.uniform(-0.02, 0.02)
    effective_gain = max(0.0, config.base_ecd_gain - config.conversion_overhead + jitter)

    return {
        "accuracy": 0.975 + random.uniform(-0.005, 0.005),
        "latency_ms": 82.0 + random.uniform(-3.0, 3.0),
        "energy_joules": 0.50 + random.uniform(-0.03, 0.03),
        "throughput_tok_sec": 12.2 + random.uniform(-0.8, 0.8),
        "ecd_improvement": effective_gain,
        "conversion_overhead": config.conversion_overhead,
        "portability_score": 0.65 + random.uniform(-0.05, 0.05),
    }
