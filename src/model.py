"""
Experiment data model.
Immutable record structures for experiments, baselines, benchmarks, and results.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import hashlib


class HorizonCategory(str, Enum):
    """Research horizon categories."""
    NEAR_TERM = "near_term"
    MID_TERM = "mid_term"
    MOONSHOT = "moonshot"


class WorkloadClass(str, Enum):
    """Workload classification."""
    DENSE_LINEAR_ALGEBRA = "dense_linear_algebra"
    SPARSE_CONDITIONAL = "sparse_conditional"
    MEMORY_BOUND = "memory_bound"
    CONTROL_HEAVY = "control_heavy"
    TEMPORAL_SENSOR = "temporal_sensor"
    END_TO_END = "end_to_end"


class Verdict(str, Enum):
    """Experiment verdict outcomes."""
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"
    PROMISING_BUT_COMPLEX = "promising_but_complex"
    INTERESTING_FOR_MOONSHOT = "interesting_for_moonshot"
    PENDING = "pending"


@dataclass
class Hardware:
    """Hardware target specification."""
    name: str
    device_type: str  # GPU, CPU, FPGA, etc.
    model: str
    arch: str
    cores: int
    memory_gb: float
    peak_power_watts: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Benchmark:
    """Benchmark definition."""
    benchmark_id: str
    name: str
    workload_class: WorkloadClass
    input_size: str
    primary_metrics: List[str]  # accuracy, latency, throughput, energy, etc.
    secondarty_metrics: List[str] = field(default_factory=list)
    quality_metric: str = "accuracy"  # primary quality metric
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0"


@dataclass
class BaselineSnapshot:
    """Immutable baseline snapshot."""
    baseline_id: str
    hardware: Hardware
    benchmark: Benchmark
    code_commit: str
    compiler_version: str
    dependency_versions: Dict[str, str]
    environment: Dict[str, str]
    created_timestamp: datetime = field(default_factory=datetime.utcnow)
    measurement_method: str = ""
    seed_policy: str = "fixed_seed_only"
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict, making datetime JSON-serializable."""
        d = asdict(self)
        d['created_timestamp'] = self.created_timestamp.isoformat()
        return d

    def hash(self) -> str:
        """Create immutable hash of baseline."""
        json_str = json.dumps(self.to_dict(), sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()


@dataclass
class EvaluationConfig:
    """Evaluation constraints and rules."""
    quality_floor: float = 0.99  # minimum acceptable quality (relative to baseline)
    latency_budget_ms_p95: float = 1000.0
    latency_budget_ms_p99: float = 2000.0
    reliability_threshold: float = 0.95  # max tolerated failure rate
    minimum_effect_threshold: float = 0.02  # minimum 2% improvement
    trials: int = 10
    confidence_level: float = 0.95
    require_holdout_pass: bool = True
    confidence_interval_excludes_zero: bool = True
    complexity_penalty_enabled: bool = True


@dataclass
class ExperimentRecord:
    """Core experiment record structure."""
    experiment_id: str
    parent_experiment_id: Optional[str] = None
    hypothesis_text: str = ""
    horizon_category: HorizonCategory = HorizonCategory.NEAR_TERM
    workload_class: WorkloadClass = WorkloadClass.DENSE_LINEAR_ALGEBRA
    hardware_target: str = ""
    representation_type: str = ""
    mutation_scope: List[str] = field(default_factory=list)
    
    # Baseline and config
    baseline_reference: str = ""
    evaluation_config: EvaluationConfig = field(default_factory=EvaluationConfig)
    benchmark_set: List[str] = field(default_factory=list)
    
    # Execution state
    created_timestamp: datetime = field(default_factory=datetime.utcnow)
    started_timestamp: Optional[datetime] = None
    completed_timestamp: Optional[datetime] = None
    
    # Results
    raw_results: Dict[str, Any] = field(default_factory=dict)
    summarized_results: Dict[str, Any] = field(default_factory=dict)
    statistical_assessment: Dict[str, Any] = field(default_factory=dict)
    verdict: Verdict = Verdict.PENDING
    
    # Reproducibility
    artifact_paths: Dict[str, str] = field(default_factory=dict)
    code_commit_hash: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        d = asdict(self)
        # Convert datetimes
        d['created_timestamp'] = self.created_timestamp.isoformat()
        if self.started_timestamp:
            d['started_timestamp'] = self.started_timestamp.isoformat()
        if self.completed_timestamp:
            d['completed_timestamp'] = self.completed_timestamp.isoformat()
        # Convert enums
        d['horizon_category'] = self.horizon_category.value
        d['workload_class'] = self.workload_class.value
        d['verdict'] = self.verdict.value
        return d

    def to_json_str(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExperimentRecord":
        """Deserialize from dict."""
        data = data.copy()
        # Parse enums
        if 'horizon_category' in data and isinstance(data['horizon_category'], str):
            data['horizon_category'] = HorizonCategory(data['horizon_category'])
        if 'workload_class' in data and isinstance(data['workload_class'], str):
            data['workload_class'] = WorkloadClass(data['workload_class'])
        if 'verdict' in data and isinstance(data['verdict'], str):
            data['verdict'] = Verdict(data['verdict'])
        # Parse evaluation config
        if 'evaluation_config' in data and isinstance(data['evaluation_config'], dict):
            data['evaluation_config'] = EvaluationConfig(**data['evaluation_config'])
        return cls(**data)


@dataclass
class MetricSet:
    """Collection of metrics from a single trial."""
    trial_num: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metrics: Dict[str, Any] = field(default_factory=dict)
    benchmark_id: str = ""
    split: str = ""
    metric_sources: Dict[str, str] = field(default_factory=dict)
    success: bool = True
    error_message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return {
            'trial_num': self.trial_num,
            'timestamp': self.timestamp.isoformat(),
            'metrics': self.metrics,
            'benchmark_id': self.benchmark_id,
            'split': self.split,
            'metric_sources': self.metric_sources,
            'success': self.success,
            'error_message': self.error_message,
        }
