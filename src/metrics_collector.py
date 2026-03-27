"""
Metrics Collector: unified metric gathering across trials and benchmarks.
Handles collection of latency, energy, throughput, quality, and area metrics.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict
import statistics
from src.model import MetricSet


class MetricsCollector:
    """
    Unified metrics collection across trials.
    
    Collects:
    - Task Quality (accuracy, F1, perplexity, etc.)
    - Latency (p50, p95, p99)
    - Throughput (ops/sec, tokens/sec, tasks/hour)
    - Energy (joules/task, watts)
    - Memory (bytes moved, cache miss rate)
    - Area / Resource (LUTs, DSP blocks, mm² estimates)
    """
    
    def __init__(self, results_dir: Path = Path("results")):
        """Initialize metrics collector."""
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory trial data
        self._trial_data: Dict[str, List[MetricSet]] = {}
    
    def record_trial(
        self,
        experiment_id: str,
        trial_num: int,
        metrics: Dict[str, Any],
        benchmark_id: str = "",
        split: str = "",
        metric_sources: Optional[Dict[str, str]] = None,
        success: bool = True,
        error_message: str = "",
    ) -> MetricSet:
        """
        Record metrics from a single trial.
        
        Args:
            experiment_id: Experiment this trial belongs to
            trial_num: Trial number (1-indexed)
            metrics: Dictionary of metric_name -> value
            success: Whether trial succeeded
            error_message: If not successful, error description
            
        Returns:
            MetricSet: The recorded metric set
        """
        metric_set = MetricSet(
            trial_num=trial_num,
            timestamp=datetime.utcnow(),
            metrics=metrics,
            benchmark_id=benchmark_id,
            split=split,
            metric_sources=metric_sources or {},
            success=success,
            error_message=error_message,
        )
        
        if experiment_id not in self._trial_data:
            self._trial_data[experiment_id] = []
        
        self._trial_data[experiment_id].append(metric_set)
        
        return metric_set
    
    def get_trial_metrics(self, experiment_id: str, trial_num: int) -> Optional[MetricSet]:
        """Get metrics for a specific trial."""
        if experiment_id not in self._trial_data:
            return None
        
        for ms in self._trial_data[experiment_id]:
            if ms.trial_num == trial_num:
                return ms
        
        return None
    
    def get_all_trials(self, experiment_id: str, split: Optional[str] = None) -> List[MetricSet]:
        """Get all trials for an experiment."""
        all_trials = self._trial_data.get(experiment_id, [])
        if split is None:
            return all_trials
        return [trial for trial in all_trials if trial.split == split]
    
    def compute_summary_stats(
        self,
        experiment_id: str,
        metric_name: str,
    ) -> Dict[str, float]:
        """
        Compute summary statistics for a metric across trials.
        
        Args:
            experiment_id: Experiment ID
            metric_name: Name of metric to summarize
            
        Returns:
            Dictionary with mean, std, min, max, p95, p99
        """
        trials = self.get_all_trials(experiment_id)
        
        values = []
        for trial in trials:
            if trial.success and metric_name in trial.metrics:
                value = trial.metrics[metric_name]
                if isinstance(value, (int, float)):
                    values.append(float(value))
        
        if not values:
            return {
                'count': 0,
                'mean': None,
                'std': None,
                'min': None,
                'max': None,
                'p95': None,
                'p99': None,
            }
        
        values_sorted = sorted(values)
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'std': statistics.stdev(values) if len(values) > 1 else 0.0,
            'min': min(values),
            'max': max(values),
            'p95': self._percentile(values_sorted, 0.95),
            'p99': self._percentile(values_sorted, 0.99),
        }
    
    def get_summarized_results(
        self,
        experiment_id: str,
        split: Optional[str] = None,
    ) -> Dict[str, Dict[str, float]]:
        """
        Get all summary statistics for all metrics in an experiment.
        
        Args:
            experiment_id: Experiment ID
            
        Returns:
            Dictionary mapping metric_name -> summary_stats
        """
        trials = self.get_all_trials(experiment_id, split=split)
        if not trials:
            return {}
        
        # Collect all metric names
        metric_names = set()
        for trial in trials:
            if trial.success:
                for metric_name, metric_value in trial.metrics.items():
                    if isinstance(metric_value, (int, float)):
                        metric_names.add(metric_name)
        
        # Compute stats for each metric
        result = {}
        for metric_name in metric_names:
            result[metric_name] = self.compute_summary_stats(experiment_id, metric_name)
        
        return result
    
    def compute_effective_compute_density(
        self,
        quality_adjusted_throughput: float,
        energy_joules: float,
        area_estimate: float,
    ) -> float:
        """
        Compute Effective Compute Density (ECD).
        
        Args:
            quality_adjusted_throughput: Work completed per second, adjusted for quality
            energy_joules: Joules consumed
            area_estimate: Silicon area (or area proxy)
            
        Returns:
            ECD = quality_adjusted_throughput / (energy_joules * area_estimate)
        """
        if energy_joules <= 0 or area_estimate <= 0:
            return 0.0
        
        return quality_adjusted_throughput / (energy_joules * area_estimate)
    
    def save_trial_data(self, experiment_id: str, path: Optional[Path] = None) -> Path:
        """
        Persist trial data to disk.
        
        Args:
            experiment_id: Experiment ID
            path: Optional custom path, default uses results_dir
            
        Returns:
            Path where data was saved
        """
        if path is None:
            path = self.results_dir / f"{experiment_id}_trials.json"
        
        trials = self.get_all_trials(experiment_id)
        trial_dicts = [asdict(trial) for trial in trials]
        
        # Convert datetimes to ISO format
        for trial_dict in trial_dicts:
            trial_dict['timestamp'] = trial_dict['timestamp'].isoformat()
        
        path.write_text(json.dumps(trial_dicts, indent=2))
        
        return path
    
    def load_trial_data(self, experiment_id: str, path: Optional[Path] = None) -> List[MetricSet]:
        """
        Load trial data from disk.
        
        Args:
            experiment_id: Experiment ID
            path: Optional custom path
            
        Returns:
            List of MetricSet objects
        """
        if path is None:
            path = self.results_dir / f"{experiment_id}_trials.json"
        
        if not path.exists():
            return []
        
        try:
            data = json.loads(path.read_text())
            
            trial_sets = []
            for item in data:
                metric_set = MetricSet(
                    trial_num=item['trial_num'],
                    metrics=item['metrics'],
                    benchmark_id=item.get('benchmark_id', ''),
                    split=item.get('split', ''),
                    metric_sources=item.get('metric_sources', {}),
                    success=item['success'],
                    error_message=item.get('error_message', ''),
                )
                trial_sets.append(metric_set)
            
            self._trial_data[experiment_id] = trial_sets
            return trial_sets
        except Exception as e:
            print(f"Error loading trial data from {path}: {e}")
            return []
    
    @staticmethod
    def _percentile(sorted_data: list, percentile: float) -> float:
        """Compute percentile of sorted data."""
        if not sorted_data:
            return 0.0
        
        index = (percentile * (len(sorted_data) - 1))
        if index == int(index):
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
