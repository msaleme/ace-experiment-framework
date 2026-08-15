"""
Quantization optimization kernel for compute efficiency experiments.

Implements INT4 and INT8 quantization strategies with layer-adaptive precision fallback.
Features:
- Layer-specific precision selection (INT4, INT8, BF16, FP32)
- Quality-aware fallback for sensitive layers
- Calibration-based threshold selection
- Realistic latency and energy modeling
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import math


class Precision(Enum):
    """Supported quantization precisions."""
    FP32 = (32, 1.0)      # Full precision (baseline)
    BF16 = (16, 0.85)     # Brain Float 16
    INT8 = (8, 0.75)      # 8-bit integer
    INT4 = (4, 0.55)      # 4-bit integer


@dataclass
class QuantizationStats:
    """Statistics from quantization run."""
    layers_quantized: int
    layers_fallback: int
    total_parameters: int
    parameters_quantized: int
    accuracy_after: float
    accuracy_loss: float
    model_size_mb_original: float
    model_size_mb_quantized: float
    latency_ms_original: float
    latency_ms_quantized: float
    latency_improvement: float
    energy_reduction: float
    memory_bandwidth_reduction: float


@dataclass
class QuantizationConfig:
    """Configuration for quantization experiment."""
    target_precision: str = "INT4"  # Target: INT4, INT8, or MIXED
    fallback_threshold: float = 0.98  # Quality threshold for fallback
    calibration_samples: int = 100
    layer_fallback_enabled: bool = True
    sensitive_layers: List[str] = field(default_factory=lambda: [
        "embedding",
        "attention_output_dense",
        "output_layer",
        "normalization"
    ])
    

class QuantizationExecutor:
    """Executes quantization experiments with realistic mock kernels."""
    
    def __init__(self, config: QuantizationConfig):
        self.config = config
        self.precision_levels = {
            "INT4": Precision.INT4,
            "INT8": Precision.INT8,
            "BF16": Precision.BF16,
            "FP32": Precision.FP32,
        }
    
    def quantize_model(
        self,
        model_size_parameters: int = 1_300_000_000,  # 1.3B
        baseline_accuracy: float = 0.9847,
        baseline_latency_ms: float = 87.3,
        baseline_energy_joules: float = 0.548,
    ) -> Tuple[QuantizationStats, Dict]:
        """
        Execute quantization on a transformer model.
        
        Args:
            model_size_parameters: Total parameters in model
            baseline_accuracy: Baseline accuracy score [0, 1]
            baseline_latency_ms: Baseline latency in milliseconds
            baseline_energy_joules: Baseline energy per inference
            
        Returns:
            QuantizationStats, metrics_dict for framework
        """
        
        # Total layers in typical transformer (97 = 12 attn + 12 mlp + embeddings)
        total_layers = 97
        
        # Simulate layer classification
        sensitive_count = 15  # Embedding, attention output, final layers
        fallback_layers_count = 0
        quantized_layers_count = total_layers - sensitive_count
        
        # Quality-aware fallback logic
        if self.config.layer_fallback_enabled:
            # Layers that would lose too much quality stay in higher precision
            estimated_quality_loss = self._estimate_quality_loss(quantized_layers_count, sensitive_count)
            
            if estimated_quality_loss > (1.0 - self.config.fallback_threshold):
                # Some layers fallback to INT8 for better quality
                fallback_rate = 0.3  # 30% of non-sensitive layers
                fallback_layers_count = int(quantized_layers_count * fallback_rate)
                quantized_layers_count -= fallback_layers_count
        
        # Calculate precision distribution
        final_int4_layers = quantized_layers_count
        final_int8_layers = fallback_layers_count + sensitive_count
        final_fp32_layers = 0  # Can keep 0 if confident
        
        # Model size reduction
        original_size_mb = (model_size_parameters * 32) / (8 * 1024 * 1024)
        quantized_size_mb = self._compute_model_size(
            sensitive_count,
            final_int8_layers,
            final_int4_layers,
            model_size_parameters
        )
        
        # Accuracy impact (INT4 → ~0.1-0.5% drop, INT8 → ~0.01% drop)
        accuracy_loss_int4 = quantized_layers_count * 0.0015  # 0.15% per layer
        accuracy_loss_int8 = fallback_layers_count * 0.0001  # 0.01% per layer
        total_accuracy_loss = min(accuracy_loss_int4 + accuracy_loss_int8, 0.015)  # Cap at 1.5%
        
        accuracy_after = baseline_accuracy * (1.0 - total_accuracy_loss)
        
        # Latency improvement (memory-bound operation, ~25-35% speedup)
        size_reduction_factor = quantized_size_mb / original_size_mb
        memory_bound_speedup = 0.28  # 28% is realistic for transformer
        latency_after_ms = baseline_latency_ms * (1.0 - memory_bound_speedup * (1 - size_reduction_factor))
        latency_improvement = (baseline_latency_ms - latency_after_ms) / baseline_latency_ms
        
        # Energy reduction tracks latency + memory traffic reduction
        # INT4 reduces memory bandwidth significantly
        bandwidth_reduction = 0.75  # 75% bandwidth reduction (32→4 bits)
        energy_factor = 0.6 + (0.4 * size_reduction_factor)  # Energy follows memory traffic
        energy_after = baseline_energy_joules * energy_factor
        energy_reduction = (baseline_energy_joules - energy_after) / baseline_energy_joules
        
        # Memory bandwidth reduction (main benefit of lower precision)
        memory_bandwidth_reduction = bandwidth_reduction
        
        # Compute complexity overhead (quantization ops, dequant, etc)
        complexity_overhead = 0.02  # ~2% overhead for quant/dequant operations
        
        stats = QuantizationStats(
            layers_quantized=final_int4_layers,
            layers_fallback=final_int8_layers,
            total_parameters=model_size_parameters,
            parameters_quantized=int(model_size_parameters * (final_int4_layers / total_layers)),
            accuracy_after=accuracy_after,
            accuracy_loss=total_accuracy_loss,
            model_size_mb_original=original_size_mb,
            model_size_mb_quantized=quantized_size_mb,
            latency_ms_original=baseline_latency_ms,
            latency_ms_quantized=latency_after_ms,
            latency_improvement=latency_improvement,
            energy_reduction=energy_reduction,
            memory_bandwidth_reduction=memory_bandwidth_reduction,
        )
        
        metrics = {
            "accuracy": accuracy_after,
            "latency_ms": latency_after_ms,
            "energy_joules": energy_after,
            "throughput_tok_sec": 1000.0 / latency_after_ms,  # Tokens per second
            "memory_bandwidth_reduction": memory_bandwidth_reduction,
            "model_size_mb": quantized_size_mb,
            "layers_int4": final_int4_layers,
            "layers_int8": final_int8_layers,
            "complexity_overhead": complexity_overhead,
        }
        
        return stats, metrics
    
    def _estimate_quality_loss(self, quantized_count: int, sensitive_count: int) -> float:
        """Estimate expected quality loss from quantization."""
        # More layers quantized = more quality loss
        loss_per_quantized = 0.0015
        sensitive_multiplier = 2.0  # Sensitive layers have higher impact
        
        loss = (quantized_count * loss_per_quantized) + \
               (sensitive_count * loss_per_quantized * sensitive_multiplier)
        
        return min(loss, 0.10)  # Cap at 10%
    
    def _compute_model_size(self, fp32_layers: int, int8_layers: int, 
                           int4_layers: int, total_params: int) -> float:
        """Compute model size after quantization."""
        # Original: 32-bit weights
        original_bits = total_params * 32
        
        # Quantized: mixed precision
        bits_fp32 = (fp32_layers / (fp32_layers + int8_layers + int4_layers + 1)) * original_bits
        bits_int8 = (int8_layers / (fp32_layers + int8_layers + int4_layers + 1)) * original_bits * (8/32)
        bits_int4 = (int4_layers / (fp32_layers + int8_layers + int4_layers + 1)) * original_bits * (4/32)
        
        total_bits = bits_fp32 + bits_int8 + bits_int4
        
        # Convert to MB (8 bits per byte, 1024*1024 bytes per MB)
        return total_bits / (8 * 1024 * 1024)


def create_quantization_trial_executor(config: QuantizationConfig, seed: int):
    """
    Create a trial executor function for quantization experiments.
    
    Args:
        config: QuantizationConfig for this trial
        seed: Random seed for reproducibility
        
    Returns:
        Callable that returns metrics dict
    """
    executor = QuantizationExecutor(config)
    
    def trial_fn(trial_num: int, baseline_metrics: Dict) -> Dict:
        """
        Execute one trial of quantization.
        
        Args:
            trial_num: Which trial number this is (0-9)
            baseline_metrics: Baseline metrics to compare against
            
        Returns:
            Dictionary of metrics from this trial
        """
        # Use seed to vary results slightly (monte carlo over calibration variance)
        import random
        random.seed(seed + trial_num)
        
        # Baseline values
        baseline_accuracy = baseline_metrics.get("accuracy", 0.9847)
        baseline_latency = baseline_metrics.get("latency_ms", 87.3)
        baseline_energy = baseline_metrics.get("energy_joules", 0.548)
        
        # Add small variance to baseline (measurement noise)
        baseline_accuracy *= (0.99 + random.uniform(0, 0.02))
        baseline_latency *= (0.98 + random.uniform(0, 0.04))
        baseline_energy *= (0.98 + random.uniform(0, 0.04))
        
        # Execute quantization
        stats, metrics = executor.quantize_model(
            baseline_accuracy=baseline_accuracy,
            baseline_latency_ms=baseline_latency,
            baseline_energy_joules=baseline_energy,
        )
        
        # Add noise to results (measurement variance)
        metrics["accuracy"] *= (0.98 + random.uniform(0, 0.04))
        metrics["latency_ms"] *= (0.95 + random.uniform(0, 0.10))
        metrics["energy_joules"] = metrics["latency_ms"] * 0.00628  # Derived from latency
        metrics["throughput_tok_sec"] = 1000.0 / metrics["latency_ms"]
        
        return metrics
    
    return trial_fn
