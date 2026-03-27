"""
Benchmark Registry: tracks all benchmarks, versions, and allowed evaluation modes.
Ensures benchmarks are immutable once published.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from src.model import Benchmark, WorkloadClass


class BenchmarkRegistry:
    """
    Maintains a registry of all benchmark definitions.
    
    Design principles:
    1. Each benchmark has a unique ID and version
    2. Benchmarks are versioned; old versions are never deleted
    3. Benchmark changes create new versions
    4. Three benchmark sets: development, validation, and holdout (never optimized on)
    """
    
    def __init__(self, registry_dir: Path = Path("configs/benchmarks")):
        """Initialize benchmark registry."""
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory registry
        self._benchmarks: Dict[str, Benchmark] = {}
        self._load_all_benchmarks()
        
        # Benchmark sets
        self._dev_set: set = set()
        self._validation_set: set = set()
        self._holdout_set: set = set()
        self._load_benchmark_sets()
    
    def register_benchmark(
        self,
        benchmark_id: str,
        name: str,
        workload_class: WorkloadClass,
        input_size: str,
        primary_metrics: List[str],
        quality_metric: str = "accuracy",
        secondary_metrics: Optional[List[str]] = None,
        version: str = "1.0",
        metadata: Optional[Dict[str, Any]] = None,
        benchmark_set: str = "development",
    ) -> Benchmark:
        """
        Register a new benchmark.
        
        Args:
            benchmark_id: Unique benchmark identifier
            name: Human-readable name
            workload_class: Classification of workload
            input_size: Description of input dimensions
            primary_metrics: List of primary metrics (e.g., ['accuracy', 'latency', 'energy'])
            quality_metric: Which metric represents quality (default: accuracy)
            secondary_metrics: Optional secondary metrics
            version: Version string (default: "1.0")
            metadata: Optional metadata dict
            benchmark_set: One of "development", "validation", "holdout"
            
        Returns:
            Benchmark: The registered benchmark
            
        Raises:
            ValueError: If benchmark already exists with same ID and version
            ValueError: If invalid benchmark_set specified
        """
        if benchmark_set not in ("development", "validation", "holdout"):
            raise ValueError(f"Invalid benchmark_set: {benchmark_set}")
        
        # Check if already exists
        key = f"{benchmark_id}_{version}"
        if key in self._benchmarks:
            raise ValueError(f"Benchmark {benchmark_id} v{version} already registered")
        
        benchmark = Benchmark(
            benchmark_id=benchmark_id,
            name=name,
            workload_class=workload_class,
            input_size=input_size,
            primary_metrics=primary_metrics,
            secondarty_metrics=secondary_metrics or [],
            quality_metric=quality_metric,
            metadata=metadata or {},
            version=version,
        )
        
        # Store
        self._benchmarks[key] = benchmark
        
        # Add to appropriate set
        if benchmark_set == "development":
            self._dev_set.add(benchmark_id)
        elif benchmark_set == "validation":
            self._validation_set.add(benchmark_id)
        elif benchmark_set == "holdout":
            self._holdout_set.add(benchmark_id)
        
        # Persist
        self._save_benchmark(benchmark)
        self._save_benchmark_sets()
        
        return benchmark
    
    def get_benchmark(self, benchmark_id: str, version: str = "latest") -> Optional[Benchmark]:
        """
        Retrieve a benchmark by ID and version.
        
        Args:
            benchmark_id: Benchmark identifier
            version: Version string, or "latest" for most recent
            
        Returns:
            Benchmark or None if not found
        """
        if version == "latest":
            # Find highest version
            matching = [
                bm for key, bm in self._benchmarks.items()
                if bm.benchmark_id == benchmark_id
            ]
            if not matching:
                return None
            # Sort by version (simplified; assumes semantic versioning)
            benchmark = sorted(matching, key=lambda b: b.version, reverse=True)[0]
            return benchmark
        else:
            key = f"{benchmark_id}_{version}"
            return self._benchmarks.get(key)
    
    def list_benchmarks(self, benchmark_set: Optional[str] = None) -> List[Benchmark]:
        """
        List all registered benchmarks.
        
        Args:
            benchmark_set: Filter by set ("development", "validation", "holdout"), or None for all
            
        Returns:
            List of Benchmark objects
        """
        if benchmark_set is None:
            return list(self._benchmarks.values())
        
        if benchmark_set == "development":
            ids = self._dev_set
        elif benchmark_set == "validation":
            ids = self._validation_set
        elif benchmark_set == "holdout":
            ids = self._holdout_set
        else:
            raise ValueError(f"Invalid benchmark_set: {benchmark_set}")
        
        # Return all versions of each ID in the set
        result = []
        for key, bm in self._benchmarks.items():
            if bm.benchmark_id in ids:
                result.append(bm)
        return result
    
    def get_benchmark_set(self, set_name: str) -> List[str]:
        """
        Get list of benchmark IDs in a specific set.
        
        Args:
            set_name: "development", "validation", or "holdout"
            
        Returns:
            List of benchmark IDs in that set
        """
        if set_name == "development":
            return list(self._dev_set)
        elif set_name == "validation":
            return list(self._validation_set)
        elif set_name == "holdout":
            return list(self._holdout_set)
        else:
            raise ValueError(f"Invalid set_name: {set_name}")
    
    def export_benchmark_metadata(self, benchmark_id: str) -> Dict[str, Any]:
        """
        Export benchmark metadata for reports.
        
        Args:
            benchmark_id: Benchmark to export
            
        Returns:
            Dictionary with benchmark information
        """
        benchmark = self.get_benchmark(benchmark_id)
        if not benchmark:
            raise FileNotFoundError(f"Benchmark {benchmark_id} not found")
        
        return asdict(benchmark)
    
    def check_benchmark_exists(self, benchmark_id: str) -> bool:
        """Check if a benchmark is registered."""
        return any(bm.benchmark_id == benchmark_id for bm in self._benchmarks.values())
    
    def _save_benchmark(self, benchmark: Benchmark) -> None:
        """Persist benchmark to disk."""
        filename = f"{benchmark.benchmark_id}_v{benchmark.version}.json"
        path = self.registry_dir / filename
        
        data = asdict(benchmark)
        data['workload_class'] = benchmark.workload_class.value
        path.write_text(json.dumps(data, indent=2))
    
    def _load_all_benchmarks(self) -> None:
        """Load all benchmarks from disk."""
        for path in self.registry_dir.glob("*.json"):
            if path.name in (
                "dev_set.json",
                "validation_set.json",
                "holdout_set.json",
                "benchmark_sets.json",
            ):
                continue
            
            try:
                data = json.loads(path.read_text())
                
                # Reconstruct WorkloadClass
                if isinstance(data['workload_class'], str):
                    data['workload_class'] = WorkloadClass(data['workload_class'])
                
                benchmark = Benchmark(**data)
                key = f"{benchmark.benchmark_id}_{benchmark.version}"
                self._benchmarks[key] = benchmark
            except Exception as e:
                print(f"Warning: Failed to load benchmark from {path}: {e}")
    
    def _save_benchmark_sets(self) -> None:
        """Persist benchmark set definitions."""
        sets = {
            'development': list(self._dev_set),
            'validation': list(self._validation_set),
            'holdout': list(self._holdout_set),
        }
        
        path = self.registry_dir / "benchmark_sets.json"
        path.write_text(json.dumps(sets, indent=2))
    
    def _load_benchmark_sets(self) -> None:
        """Load benchmark set definitions."""
        path = self.registry_dir / "benchmark_sets.json"
        if path.exists():
            try:
                sets = json.loads(path.read_text())
                self._dev_set = set(sets.get('development', []))
                self._validation_set = set(sets.get('validation', []))
                self._holdout_set = set(sets.get('holdout', []))
            except Exception as e:
                print(f"Warning: Failed to load benchmark sets: {e}")
