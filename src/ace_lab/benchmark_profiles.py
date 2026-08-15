"""Access immutable benchmark profiles packaged with ACE.

These profiles are part of the experiment contract.  Loading them through
``importlib.resources`` keeps the installed-wheel behavior independent of the
source checkout layout.
"""

from __future__ import annotations

from importlib import resources
from typing import Any, Dict

import yaml


def load_benchmark_profile(benchmark_id: str) -> Dict[str, Any]:
    """Return a packaged benchmark profile by identifier.

    Only simple benchmark identifiers are accepted.  This prevents a caller
    from escaping the packaged resource directory through a path-like value.
    """
    if not benchmark_id or benchmark_id != benchmark_id.replace("/", "").replace("\\", ""):
        raise ValueError("benchmark_id must be a simple packaged profile identifier")

    profile = resources.files("ace_lab").joinpath("resources", "benchmarks", f"{benchmark_id}.yaml")
    if not profile.is_file():
        raise ValueError(f"unknown packaged benchmark profile: {benchmark_id}")

    loaded = yaml.safe_load(profile.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict) or loaded.get("benchmark_id") != benchmark_id:
        raise ValueError(f"invalid packaged benchmark profile: {benchmark_id}")
    return loaded
