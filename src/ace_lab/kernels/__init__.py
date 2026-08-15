"""
ACE Experiment Framework - Phase 2 Kernel Modules

Optimization kernels for computing efficiency experiments:
- quantization: INT4/INT8 precision reduction
- sparsity: Token pruning and dynamic sparsity
- memory_optimization: Activation checkpointing and recomputation
- compiler_optimization: Kernel fusion and graph optimization
"""

__version__ = "0.2.0"
__all__ = [
    "quantization",
    "sparsity", 
    "memory_optimization",
    "compiler_optimization",
]
