"""
Baseline Manager: creates and manages immutable baseline snapshots.
Enforces that baselines cannot be modified once created.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import asdict
from src.model import BaselineSnapshot, Hardware, Benchmark


class BaselineManager:
    """
    Freezes immutable baseline snapshots.
    
    Rules:
    1. Once created, baselines cannot be modified
    2. All baselines are versioned and timestamped
    3. Hash verification ensures integrity
    4. Baseline metadata includes full environment record
    """
    
    def __init__(self, baselines_dir: Path = Path("baselines")):
        """Initialize baseline manager."""
        self.baselines_dir = Path(baselines_dir)
        self.baselines_dir.mkdir(parents=True, exist_ok=True)
        self._loaded_baselines: Dict[str, BaselineSnapshot] = {}
    
    def create_baseline(
        self,
        baseline_id: str,
        hardware: Hardware,
        benchmark: Benchmark,
        code_commit: str,
        compiler_version: str,
        dependency_versions: Dict[str, str],
        environment: Dict[str, str],
        measurement_method: str = "",
        seed_policy: str = "fixed_seed_only",
        notes: str = "",
    ) -> BaselineSnapshot:
        """
        Create a new immutable baseline.
        
        Args:
            baseline_id: Unique identifier (e.g., "baseline_gpu_transformer_bf16_v1")
            hardware: Hardware specification
            benchmark: Benchmark specification
            code_commit: Git commit hash
            compiler_version: Compiler/framework version
            dependency_versions: All critical dependencies and versions
            environment: Full environment variables
            measurement_method: How metrics were collected
            seed_policy: Seed strategy (fixed_seed_only, random_sweep, etc.)
            notes: Optional notes
            
        Returns:
            BaselineSnapshot: The created baseline
            
        Raises:
            ValueError: If baseline already exists
        """
        baseline_path = self.baselines_dir / f"{baseline_id}.json"
        
        if baseline_path.exists():
            raise ValueError(f"Baseline {baseline_id} already exists. Baselines are immutable.")
        
        # Create baseline snapshot
        baseline = BaselineSnapshot(
            baseline_id=baseline_id,
            hardware=hardware,
            benchmark=benchmark,
            code_commit=code_commit,
            compiler_version=compiler_version,
            dependency_versions=dependency_versions,
            environment=environment,
            created_timestamp=datetime.utcnow(),
            measurement_method=measurement_method,
            seed_policy=seed_policy,
            notes=notes,
        )
        
        # Persist baseline
        self._save_baseline(baseline, baseline_path)
        
        # Cache it
        self._loaded_baselines[baseline_id] = baseline
        
        return baseline
    
    def get_baseline(self, baseline_id: str) -> Optional[BaselineSnapshot]:
        """
        Load a baseline by ID.
        
        Args:
            baseline_id: Baseline identifier
            
        Returns:
            BaselineSnapshot or None if not found
        """
        # Check cache first
        if baseline_id in self._loaded_baselines:
            return self._loaded_baselines[baseline_id]
        
        # Try to load from disk
        baseline_path = self.baselines_dir / f"{baseline_id}.json"
        if not baseline_path.exists():
            return None
        
        baseline = self._load_baseline(baseline_path)
        self._loaded_baselines[baseline_id] = baseline
        return baseline
    
    def list_baselines(self) -> list[str]:
        """List all available baseline IDs."""
        baseline_files = list(self.baselines_dir.glob("*.json"))
        return [f.stem for f in baseline_files]
    
    def verify_baseline_integrity(self, baseline_id: str) -> bool:
        """
        Verify that a baseline hasn't been tampered with.
        
        Args:
            baseline_id: Baseline to verify
            
        Returns:
            True if integrity check passes
            
        Raises:
            FileNotFoundError: If baseline not found
            ValueError: If baseline is corrupted
        """
        baseline_path = self.baselines_dir / f"{baseline_id}.json"
        if not baseline_path.exists():
            raise FileNotFoundError(f"Baseline {baseline_id} not found")
        
        baseline = self._load_baseline(baseline_path)
        expected_hash = baseline.hash()
        
        # Load hash file if it exists
        hash_path = self.baselines_dir / f"{baseline_id}.hash"
        if hash_path.exists():
            stored_hash = hash_path.read_text().strip()
            if stored_hash != expected_hash:
                raise ValueError(f"Baseline {baseline_id} integrity check failed")
        
        return True
    
    def export_baseline_metadata(self, baseline_id: str) -> Dict[str, Any]:
        """
        Export baseline metadata for reports and documentation.
        
        Args:
            baseline_id: Baseline to export
            
        Returns:
            Dictionary with all baseline information
        """
        baseline = self.get_baseline(baseline_id)
        if not baseline:
            raise FileNotFoundError(f"Baseline {baseline_id} not found")
        
        return {
            'baseline_id': baseline.baseline_id,
            'hardware': asdict(baseline.hardware),
            'benchmark': asdict(baseline.benchmark),
            'code_commit': baseline.code_commit,
            'compiler_version': baseline.compiler_version,
            'dependency_versions': baseline.dependency_versions,
            'created_timestamp': baseline.created_timestamp.isoformat(),
            'measurement_method': baseline.measurement_method,
            'seed_policy': baseline.seed_policy,
            'baseline_hash': baseline.hash(),
            'notes': baseline.notes,
        }
    
    def _save_baseline(self, baseline: BaselineSnapshot, path: Path) -> None:
        """
        Persist baseline to disk with integrity hash.
        
        Args:
            baseline: Baseline to save
            path: Path to save to
        """
        # Save JSON
        baseline_dict = baseline.to_dict()
        path.write_text(json.dumps(baseline_dict, indent=2))
        
        # Save hash for integrity verification
        hash_path = path.parent / f"{path.stem}.hash"
        hash_value = baseline.hash()
        hash_path.write_text(hash_value)
    
    def _load_baseline(self, path: Path) -> BaselineSnapshot:
        """
        Load baseline from disk.
        
        Args:
            path: Path to baseline JSON file
            
        Returns:
            BaselineSnapshot
        """
        data = json.loads(path.read_text())
        
        # Reconstruct Hardware
        hw_data = data['hardware']
        hardware = Hardware(**hw_data)
        
        # Reconstruct Benchmark
        bm_data = data['benchmark']
        benchmark = Benchmark(**bm_data)
        
        # Create BaselineSnapshot
        baseline = BaselineSnapshot(
            baseline_id=data['baseline_id'],
            hardware=hardware,
            benchmark=benchmark,
            code_commit=data['code_commit'],
            compiler_version=data['compiler_version'],
            dependency_versions=data['dependency_versions'],
            environment=data['environment'],
            measurement_method=data.get('measurement_method', ''),
            seed_policy=data.get('seed_policy', 'fixed_seed_only'),
            notes=data.get('notes', ''),
        )
        
        return baseline
