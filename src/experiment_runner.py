"""
Experiment Runner: orchestrates experiment execution with proper constraints and lifecycle.
Enforces mutation scope, trial limits, and resource budgets.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import time
from src.model import ExperimentRecord, Verdict
from src.baseline_manager import BaselineManager
from src.benchmark_registry import BenchmarkRegistry
from src.metrics_collector import MetricsCollector


class ExperimentRunner:
    """
    Orchestrates experiments with proper controls.
    
    Responsibilities:
    1. Load experiment config
    2. Freeze baseline
    3. Enforce mutation scope
    4. Run repeated trials
    5. Collect metrics
    6. Track execution lifecycle
    """
    
    def __init__(
        self,
        baseline_manager: BaselineManager,
        benchmark_registry: BenchmarkRegistry,
        metrics_collector: MetricsCollector,
        experiments_dir: Path = Path("experiments"),
    ):
        """Initialize experiment runner."""
        self.baseline_manager = baseline_manager
        self.benchmark_registry = benchmark_registry
        self.metrics_collector = metrics_collector
        self.experiments_dir = Path(experiments_dir)
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory experiment records
        self._experiments: Dict[str, ExperimentRecord] = {}
    
    def load_experiment_config(self, config_path: Path) -> ExperimentRecord:
        """
        Load an experiment from YAML config file.
        
        Args:
            config_path: Path to experiment YAML/JSON config
            
        Returns:
            ExperimentRecord parsed from config
        """
        import yaml
        
        if config_path.suffix == '.yaml' or config_path.suffix == '.yml':
            with open(config_path) as f:
                config_dict = yaml.safe_load(f)
        elif config_path.suffix == '.json':
            with open(config_path) as f:
                config_dict = json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")
        
        # Create ExperimentRecord from config
        experiment = ExperimentRecord.from_dict(config_dict)
        self._experiments[experiment.experiment_id] = experiment
        
        return experiment
    
    def create_experiment(
        self,
        experiment_id: str,
        hypothesis_text: str,
        horizon_category,
        workload_class,
        hardware_target: str,
        representation_type: str,
        mutation_scope: List[str],
        baseline_reference: str,
        benchmark_set: List[str],
        evaluation_config=None,
        parent_experiment_id: Optional[str] = None,
        notes: str = "",
    ) -> ExperimentRecord:
        """
        Create a new experiment record.
        
        Args:
            experiment_id: Unique experiment identifier
            hypothesis_text: Single sentence hypothesis
            horizon_category: Near-term, mid-term, or moonshot
            workload_class: Classification of workload
            hardware_target: Target hardware (e.g., "A100")
            representation_type: Data representation (e.g., "INT4", "BF16")
            mutation_scope: List of what can be changed (e.g., ["quantization_config"])
            baseline_reference: Reference to baseline snapshot ID
            benchmark_set: List of benchmarks to test on
            evaluation_config: EvaluationConfig instance
            parent_experiment_id: Parent experiment if branched from another
            notes: Optional notes
            
        Returns:
            ExperimentRecord: Created experiment record
            
        Raises:
            ValueError: If baseline doesn't exist
            ValueError: If any benchmark doesn't exist
        """
        # Verify baseline exists
        baseline = self.baseline_manager.get_baseline(baseline_reference)
        if not baseline:
            raise ValueError(f"Baseline {baseline_reference} not found")
        
        # Verify benchmarks exist
        for benchmark_id in benchmark_set:
            if not self.benchmark_registry.check_benchmark_exists(benchmark_id):
                raise ValueError(f"Benchmark {benchmark_id} not registered")
        
        # Create record
        experiment = ExperimentRecord(
            experiment_id=experiment_id,
            parent_experiment_id=parent_experiment_id,
            hypothesis_text=hypothesis_text,
            horizon_category=horizon_category,
            workload_class=workload_class,
            hardware_target=hardware_target,
            representation_type=representation_type,
            mutation_scope=mutation_scope,
            baseline_reference=baseline_reference,
            benchmark_set=benchmark_set,
            evaluation_config=evaluation_config,
            created_timestamp=datetime.utcnow(),
            notes=notes,
        )
        
        self._experiments[experiment_id] = experiment
        
        return experiment
    
    def run_experiment(
        self,
        experiment_id: str,
        trial_executor: Callable[[int, str], Dict[str, float]],
        dry_run: bool = False,
    ) -> ExperimentRecord:
        """
        Execute an experiment with repeated trials.
        
        Args:
            experiment_id: Experiment to run
            trial_executor: Function(trial_num, benchmark_id) -> Dict[metric_name, value]
            dry_run: If True, don't actually run trials
            
        Returns:
            Updated ExperimentRecord
            
        Raises:
            KeyError: If experiment not found
            RuntimeError: If trial execution fails
        """
        experiment = self.get_experiment(experiment_id)
        if not experiment:
            raise KeyError(f"Experiment {experiment_id} not found")
        
        # Mark as started
        experiment.started_timestamp = datetime.utcnow()
        
        if dry_run:
            experiment.completed_timestamp = datetime.utcnow()
            return experiment
        
        # Run trials independently for development/validation/holdout
        num_trials = experiment.evaluation_config.trials
        split_map = self._resolve_benchmark_splits(experiment)
        execution_trace: Dict[str, Any] = {}
        trial_counter = 0

        for split in ("development", "validation", "holdout"):
            benchmarks = split_map.get(split, [])
            execution_trace[split] = {
                "benchmarks": list(benchmarks),
                "configured": len(benchmarks) > 0,
                "executed_trials": 0,
                "missing": len(benchmarks) == 0,
            }

            for benchmark_id in benchmarks:
                for _ in range(num_trials):
                    trial_counter += 1
                    try:
                        metrics = trial_executor(trial_counter, benchmark_id)
                        metric_sources = metrics.pop("metric_sources", {}) if isinstance(metrics, dict) else {}

                        self.metrics_collector.record_trial(
                            experiment_id=experiment_id,
                            trial_num=trial_counter,
                            metrics=metrics,
                            benchmark_id=benchmark_id,
                            split=split,
                            metric_sources=metric_sources,
                            success=True,
                        )
                        execution_trace[split]["executed_trials"] += 1

                    except Exception as e:
                        self.metrics_collector.record_trial(
                            experiment_id=experiment_id,
                            trial_num=trial_counter,
                            metrics={},
                            benchmark_id=benchmark_id,
                            split=split,
                            metric_sources={},
                            success=False,
                            error_message=str(e),
                        )
        
        # Mark as completed
        experiment.completed_timestamp = datetime.utcnow()
        
        # Compute summary statistics
        summary = self.metrics_collector.get_summarized_results(experiment_id)
        experiment.summarized_results = summary
        experiment.raw_results.setdefault("gate_runs", {})
        experiment.raw_results["gate_runs"] = execution_trace
        experiment.raw_results["split_summaries"] = {
            split: self.metrics_collector.get_summarized_results(experiment_id, split=split)
            for split in ("development", "validation", "holdout")
        }
        
        # Save trial data
        self.metrics_collector.save_trial_data(experiment_id)
        
        return experiment

    def _resolve_benchmark_splits(self, experiment: ExperimentRecord) -> Dict[str, List[str]]:
        configured = experiment.raw_results.get("benchmark_sets", {}) if experiment.raw_results else {}

        if configured:
            return {
                "development": list(configured.get("development", [])),
                "validation": list(configured.get("validation", [])),
                "holdout": list(configured.get("holdout", [])),
            }

        split_map = {"development": [], "validation": [], "holdout": []}
        for benchmark_id in experiment.benchmark_set:
            if benchmark_id in self.benchmark_registry.get_benchmark_set("development"):
                split_map["development"].append(benchmark_id)
            elif benchmark_id in self.benchmark_registry.get_benchmark_set("validation"):
                split_map["validation"].append(benchmark_id)
            elif benchmark_id in self.benchmark_registry.get_benchmark_set("holdout"):
                split_map["holdout"].append(benchmark_id)

        return split_map
    
    def get_experiment(self, experiment_id: str) -> Optional[ExperimentRecord]:
        """Get an experiment record by ID."""
        return self._experiments.get(experiment_id)
    
    def list_experiments(self) -> List[ExperimentRecord]:
        """List all experiments."""
        return list(self._experiments.values())
    
    def verify_mutation_scope(
        self,
        experiment_id: str,
        changed_items: List[str],
    ) -> bool:
        """
        Verify that only declared mutations were made.
        
        Args:
            experiment_id: Experiment ID
            changed_items: List of things that were changed
            
        Returns:
            True if all changes are within declared scope
            
        Raises:
            ValueError: If changes exceed scope
        """
        experiment = self.get_experiment(experiment_id)
        if not experiment:
            raise KeyError(f"Experiment {experiment_id} not found")
        
        allowed_scope = set(experiment.mutation_scope)
        actual_changes = set(changed_items)
        
        invalid_changes = actual_changes - allowed_scope
        
        if invalid_changes:
            raise ValueError(
                f"Changes exceed declared scope: {invalid_changes}. "
                f"Allowed: {allowed_scope}"
            )
        
        return True
    
    def save_experiment(self, experiment_id: str, path: Optional[Path] = None) -> Path:
        """
        Persist experiment record to disk.
        
        Args:
            experiment_id: Experiment ID
            path: Optional custom path
            
        Returns:
            Path where experiment was saved
        """
        experiment = self.get_experiment(experiment_id)
        if not experiment:
            raise KeyError(f"Experiment {experiment_id} not found")
        
        if path is None:
            path = self.experiments_dir / f"{experiment_id}.json"
        
        json_str = experiment.to_json_str(indent=2)
        path.write_text(json_str)
        
        return path
    
    def load_experiment(self, experiment_id: str, path: Optional[Path] = None) -> ExperimentRecord:
        """
        Load experiment record from disk.
        
        Args:
            experiment_id: Experiment ID
            path: Optional custom path
            
        Returns:
            ExperimentRecord
        """
        if path is None:
            path = self.experiments_dir / f"{experiment_id}.json"
        
        if not path.exists():
            raise FileNotFoundError(f"Experiment file not found: {path}")
        
        data = json.loads(path.read_text())
        experiment = ExperimentRecord.from_dict(data)
        
        self._experiments[experiment_id] = experiment
        
        return experiment
