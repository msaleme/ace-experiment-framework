"""
ACE Experiment Framework - Main Package
Automated Compute Efficiency Experimental Lab
"""

from src.model import (
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

from src.baseline_manager import BaselineManager
from src.benchmark_registry import BenchmarkRegistry
from src.metrics_collector import MetricsCollector
from src.experiment_runner import ExperimentRunner
from src.stats_evaluator import StatsEvaluator
from src.results_store import ResultsStore
from src.report_generator import ReportGenerator

__version__ = "0.1.0"
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
