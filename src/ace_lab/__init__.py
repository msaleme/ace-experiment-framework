"""
ACE Experiment Framework - Main Package
Automated Compute Efficiency Experimental Lab
"""

from ace_lab.model import (
    HorizonCategory,
    WorkloadClass,
    Verdict,
    Hardware,
    Benchmark,
    BaselineSnapshot,
    EvaluationConfig,
    ExperimentRecord,
    MetricSet,
)

from ace_lab.baseline_manager import BaselineManager
from ace_lab.benchmark_registry import BenchmarkRegistry
from ace_lab.metrics_collector import MetricsCollector
from ace_lab.experiment_runner import ExperimentRunner
from ace_lab.stats_evaluator import StatsEvaluator
from ace_lab.results_store import ResultsStore
from ace_lab.report_generator import ReportGenerator

__version__ = "0.1.3"
__all__ = [
    # Enums
    "HorizonCategory",
    "WorkloadClass",
    "Verdict",
    # Models
    "Hardware",
    "Benchmark",
    "BaselineSnapshot",
    "EvaluationConfig",
    "ExperimentRecord",
    "MetricSet",
    # Managers
    "BaselineManager",
    "BenchmarkRegistry",
    "MetricsCollector",
    "ExperimentRunner",
    "StatsEvaluator",
    "ResultsStore",
    "ReportGenerator",
]
