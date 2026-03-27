"""
Results Store: structured persistence and retrieval of experiment results.
Supports searching, filtering, and comparison queries.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.model import ExperimentRecord, Verdict


class ResultsStore:
    """
    Persistent store for experiment results.
    
    Responsibilities:
    1. Save experiment records immutably
    2. Index experiments for quick lookup
    3. Support filtering and search queries
    4. Enable comparison across experiments
    5. Detect duplicate/equivalent experiments
    """
    
    def __init__(self, store_dir: Path = Path("results")):
        """Initialize results store."""
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)
        
        self._index_path = self.store_dir / "index.json"
        self._index: Dict[str, str] = {}  # experiment_id -> filepath
        self._load_index()
    
    def save_experiment(self, experiment: ExperimentRecord) -> Path:
        """
        Save an experiment record immutably.
        
        Args:
            experiment: ExperimentRecord to save
            
        Returns:
            Path where experiment was saved
        """
        exp_dir = self.store_dir / experiment.experiment_id
        exp_dir.mkdir(parents=True, exist_ok=True)
        
        # Save main record
        exp_path = exp_dir / "experiment.json"
        json_str = experiment.to_json_str(indent=2)
        exp_path.write_text(json_str)
        
        # Update index
        self._index[experiment.experiment_id] = str(exp_path)
        self._save_index()
        
        return exp_path
    
    def load_experiment(self, experiment_id: str) -> Optional[ExperimentRecord]:
        """
        Load an experiment by ID.
        
        Args:
            experiment_id: Experiment identifier
            
        Returns:
            ExperimentRecord or None if not found
        """
        if experiment_id not in self._index:
            return None
        
        path = Path(self._index[experiment_id])
        if not path.exists():
            return None
        
        try:
            data = json.loads(path.read_text())
            return ExperimentRecord.from_dict(data)
        except Exception as e:
            print(f"Error loading experiment {experiment_id}: {e}")
            return None
    
    def query_by_hypothesis(self, partial_text: str) -> List[ExperimentRecord]:
        """
        Find experiments by hypothesis text (partial match).
        
        Args:
            partial_text: Text to search for in hypothesis
            
        Returns:
            List of matching experiments
        """
        results = []
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if exp and partial_text.lower() in exp.hypothesis_text.lower():
                results.append(exp)
        return results
    
    def query_by_verdict(self, verdict: Verdict) -> List[ExperimentRecord]:
        """
        Find experiments by verdict.
        
        Args:
            verdict: Verdict to search for
            
        Returns:
            List of experiments with that verdict
        """
        results = []
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if exp and exp.verdict == verdict:
                results.append(exp)
        return results
    
    def query_by_horizon(self, horizon) -> List[ExperimentRecord]:
        """
        Find experiments by horizon category.
        
        Args:
            horizon: Horizon category
            
        Returns:
            List of experiments in that horizon
        """
        results = []
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if exp and exp.horizon_category == horizon:
                results.append(exp)
        return results
    
    def query_by_baseline(self, baseline_id: str) -> List[ExperimentRecord]:
        """
        Find all experiments that used a specific baseline.
        
        Args:
            baseline_id: Baseline identifier
            
        Returns:
            List of experiments using that baseline
        """
        results = []
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if exp and exp.baseline_reference == baseline_id:
                results.append(exp)
        return results
    
    def find_branched_experiments(self, parent_id: str) -> List[ExperimentRecord]:
        """
        Find all experiments that branched from a parent.
        
        Args:
            parent_id: Parent experiment ID
            
        Returns:
            List of child experiments
        """
        results = []
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if exp and exp.parent_experiment_id == parent_id:
                results.append(exp)
        return results
    
    def find_similar_experiments(
        self,
        horizon=None,
        workload_class=None,
        hardware=None,
        max_results: int = 10,
    ) -> List[ExperimentRecord]:
        """
        Find similar experiments by matching criteria.
        
        Args:
            horizon: Horizon category to match
            workload_class: Workload class to match
            hardware: Hardware target to match
            max_results: Maximum results to return
            
        Returns:
            List of matching experiments
        """
        results = []
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if not exp:
                continue
            
            match = True
            if horizon and exp.horizon_category != horizon:
                match = False
            if workload_class and exp.workload_class != workload_class:
                match = False
            if hardware and exp.hardware_target != hardware:
                match = False
            
            if match:
                results.append(exp)
            
            if len(results) >= max_results:
                break
        
        return results
    
    def list_experiments(self, limit: Optional[int] = None) -> List[ExperimentRecord]:
        """
        List all experiments.
        
        Args:
            limit: Maximum number to return
            
        Returns:
            List of experiments
        """
        results = []
        for i, exp_id in enumerate(self._index):
            if limit and i >= limit:
                break
            exp = self.load_experiment(exp_id)
            if exp:
                results.append(exp)
        return results
    
    def count_by_verdict(self) -> Dict[str, int]:
        """
        Count experiments by verdict.
        
        Returns:
            Dictionary mapping verdict -> count
        """
        counts = {v.value: 0 for v in Verdict}
        for exp_id in self._index:
            exp = self.load_experiment(exp_id)
            if exp:
                counts[exp.verdict.value] += 1
        return counts
    
    def export_summary(self) -> Dict[str, Any]:
        """
        Export summary statistics about all experiments.
        
        Returns:
            Dictionary with summary information
        """
        experiments = self.list_experiments()
        
        return {
            'total_experiments': len(experiments),
            'by_verdict': self.count_by_verdict(),
            'by_horizon': {h: len(self.query_by_horizon(h)) for h in self.query_by_horizon.__code__.co_consts},
            'total_trials': sum(
                exp.evaluation_config.trials
                for exp in experiments
                if exp.evaluation_config
            ),
        }
    
    def _load_index(self) -> None:
        """Load index from disk."""
        if self._index_path.exists():
            try:
                self._index = json.loads(self._index_path.read_text())
            except Exception as e:
                print(f"Error loading index: {e}")
                self._index = {}
        else:
            # Build index from scratch
            self._build_index()
    
    def _save_index(self) -> None:
        """Persist index to disk."""
        self._index_path.write_text(json.dumps(self._index, indent=2))
    
    def _build_index(self) -> None:
        """Rebuild index from experiment files on disk."""
        self._index = {}
        for exp_dir in self.store_dir.iterdir():
            if exp_dir.is_dir():
                exp_file = exp_dir / "experiment.json"
                if exp_file.exists():
                    self._index[exp_dir.name] = str(exp_file)
        self._save_index()
