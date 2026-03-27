# Phase 2 Implementation Guide

## Overview

Phase 1 is complete. Phase 2 implements the first 4 experiments on existing hardware - the "fast path to real signal."

These 4 experiments represent the near-term lane and are designed to:
1. Validate the experimental lab infrastructure
2. Produce measurable wins on real hardware
3. Establish credible baselines for future work
4. Prove the framework's controls work correctly

## Experiment 1: Adaptive INT4/INT8 Quantization

**Hypothesis**: Layer-adaptive INT4 quantization with BF16 fallback improves ECD by at least 15% on transformer inference without violating the 99% quality floor.

**Mutation Scope**:
- `quantization_config`: Which layers, which precision levels
- `fallback_policy`: Conditions for falling back to BF16
- `layer_fallback_thresholds`: Quality thresholds per layer

**Expected Implementation**:
```python
# Location: src/kernels/quantization.py

class QuantizationStrategy:
    def quantize_layer(self, layer, precision, fallback_threshold):
        """Quantize a layer, fall back to BF16 if quality drops below threshold"""
        quantized = quantize_to_precision(layer, precision)
        quality_loss = measure_quality_loss(quantized)
        
        if quality_loss > fallback_threshold:
            return layer.to_bfloat16()  # Fallback
        return quantized
    
    def compute_layer_precision_map(self, model, quality_floor):
        """Adaptive precision assignment per layer"""
        # Fine binary search for minimum viable precision per layer
        # Returns: {layer_name: precision}
        pass

class INT4Executor:
    """Trial executor for INT4 experiments"""
    def run_trial(self, trial_num, benchmark_id):
        # 1. Load model at baseline precision (BF16)
        # 2. Apply adaptive quantization config
        # 3. Inference on benchmark
        # 4. Measure: accuracy, latency, energy, throughput
        # 5. Return metrics dict
        pass
```

**Metrics to Track**:
- `accuracy`: Must remain >= 99% of baseline
- `latency_ms_p95`: Measure inference p95
- `energy_joules`: Per-inference energy (RAPL + GPU)
- `throughput_tok_sec`: Tokens per second
- `ecd_estimate`: (quality × throughput) / (energy × 1.0 area_proxy)

**Trials**: 10 (repeated runs with different random seeds)

**Quality Floor**: 99% of baseline accuracy

**Latency Budget**: p95 <= 120ms

**Data**: Transformer model inference on 128-token sequences, batch=1

---

## Experiment 2: Dynamic Sparsity / Token Pruning

**Hypothesis**: Dynamic token pruning reduces average energy per prompt by at least 20% while preserving response quality on long-context tasks.

**Mutation Scope**:
- `pruning_threshold`: Token importance threshold for keeping a token
- `pruning_method`: Which importance scoring method (gradient, magnitude, entropy)
- `context_length`: Length of context to evaluate pruning on

**Expected Implementation**:
```python
# Location: src/kernels/sparsity.py

class TokenPruner:
    def score_token_importance(self, token, context, method="gradient"):
        """Score how important a token is for output"""
        if method == "gradient":
            # Compute gradient of loss w.r.t. this token embedding
            return compute_gradient_magnitude(token)
        elif method == "magnitude":
            # Use embedding magnitude as proxy
            return token.norm()
        elif method == "entropy":
            # Attention entropy over this token
            return compute_attention_entropy(token, context)

    def prune_sequence(self, sequence, threshold, budget=0.9):
        """Remove unimportant tokens from context sequence"""
        scores = [self.score_token_importance(t, sequence) for t in sequence]
        keep_indices = [i for i, s in enumerate(scores) if s >= threshold]
        
        # Ensure we keep at least budget% of tokens
        if len(keep_indices) < len(sequence) * budget:
            keep_indices = sorted(range(len(sequence)), 
                                key=lambda i: scores[i], 
                                reverse=True)[:int(len(sequence)*budget)]
        
        return sequence[keep_indices]

class TokenPruningExecutor:
    """Trial executor for sparsity experiments"""
    def run_trial(self, trial_num, benchmark_id):
        # 1. Load long-context task (e.g., summarization)
        # 2. For each prompt:
        #    a. Score tokens
        #    b. Prune low-importance tokens
        #    c. Run inference on pruned context
        # 3. Measure accuracy, latency, energy
        return metrics
```

**Metrics to Track**:
- `accuracy_f1`: F1 score on task (e.g., ROUGE for summarization)
- `tokens_pruned_pct`: Percentage of tokens removed
- `latency_ms_p95`: End-to-end latency
- `energy_joules`: Total energy for inference
- `ecd_estimate`: (quality × throughput) / energy

**Trials**: 10 on diverse long-context datasets

**Quality Floor**: 95% of baseline accuracy (more lenient since pruning intentionally changes output)

**Latency Budget**: p95 <= 150ms (context-dependent)

---

## Experiment 3: Memory-Traffic Reduction

**Hypothesis**: Activation recomputation optimizes the storage-vs.-recomputation tradeoff, reducing memory bandwidth by at least 25% without exceeding latency budget.

**Mutation Scope**:
- `recomputation_layers`: Which layers to recompute activations for
- `memory_budget_mb`: Maximum memory for storing activations
- `recomputation_granularity`: At what kernel granularity to recompute

**Expected Implementation**:
```python
# Location: src/kernels/memory_optimization.py

class ActivationMemoryOptimizer:
    def estimate_memory_footprint(self, model, batch_size, seq_len):
        """Estimate activation memory for full storage"""
        # Sum activation sizes per layer
        total = 0
        for layer in model.layers:
            act_size = batch_size * seq_len * layer.hidden_dim * 4  # fp32
            total += act_size
        return total

    def select_recomputation_schedule(self, model, memory_budget):
        """Decide which layers to recompute vs. store"""
        schedule = {}
        cumulative_memory = 0
        
        for layer in model.layers:
            recompute_cost = estimate_recomputation_latency(layer)
            memory_cost = estimate_activation_footprint(layer)
            
            if cumulative_memory + memory_cost <= memory_budget:
                schedule[layer.name] = "store"
                cumulative_memory += memory_cost
            else:
                schedule[layer.name] = "recompute"
        
        return schedule

    def optimize_memory_layout(self, model, batch_size, seq_len):
        """Reorganize memory access patterns for cache efficiency"""
        # Reorder activation storage for better spatial locality
        # Prefetch activations based on access patterns
        pass

class MemoryOptimizationExecutor:
    """Trial executor for memory experiments"""
    def run_trial(self, trial_num, benchmark_id):
        # 1. Profile baseline activation memory
        # 2. Apply recomputation schedule
        # 3. Measure latency during recomputation
        # 4. Measure DRAM bandwidth and cache hits
        # 5. Return metrics
        return {
            "memory_traffic_bytes": total_bytes_moved,
            "cache_hit_rate": hits / total_accesses,
            "latency_ms": end_to_end_latency,
            "energy_joules": energy_consumed,
        }
```

**Metrics to Track**:
- `memory_traffic_bytes`: Total bytes moved between DRAM and cache
- `dram_bandwidth_utilized`: Peak BW / system BW
- `latency_ms_p95`: Inference latency
- `energy_joules`: Total energy
- `cache_hit_rate`: L3 cache hit percentage

**Trials**: 10

**Quality Floor**: N/A (numerical output identical)

**Latency Budget**: p95 <= 130ms (may increase due to recomputation)

---

## Experiment 4: Compiler Graph Optimization

**Hypothesis**: Kernel fusion and graph-level tiling reduce memory movement and improve p95 latency by at least 15% on dense linear algebra workloads.

**Mutation Scope**:
- `fusion_rules`: Which kernels to fuse
- `tiling_config`: Tile sizes for loop tiling
- `instruction_scheduling`: Kernel scheduling strategy

**Expected Implementation**:
```python
# Location: src/kernels/compiler_optimization.py

class KernelGraphOptimizer:
    def identify_fusion_opportunities(self, graph):
        """Find kernels that can be fused"""
        # Look for:
        # - Elementwise operations (can fuse)
        # - Sequential kernels sharing memory (can fuse)
        # - Chains of small kernels (definitely fuse)
        fusion_groups = []
        # Return list of kernel groups to fuse
        return fusion_groups

    def compute_optimal_tiling(self, kernel, hardware):
        """Compute optimal tile sizes for loop tiling"""
        # Tile for cache line size, L1, L2, L3
        # Minimize memory traffic while maximizing ILP
        tile_config = {
            "M": optimal_m,
            "N": optimal_n,
            "K": optimal_k,
        }
        return tile_config

    def fuse_kernels(self, kernel_list):
        """Fuse multiple kernels into single optimized kernel"""
        # Generate fused kernel code
        # Inline data between kernels
        # Share temporary buffers
        fused_kernel = generate_fused_kernel_code(kernel_list)
        return fused_kernel

class CompilerOptimizationExecutor:
    """Trial executor for compiler experiments"""
    def run_trial(self, trial_num, benchmark_id):
        # 1. Analyze computational graph
        # 2. Apply fusion rules
        # 3. Apply tiling config
        # 4. Compile and benchmark
        # 5. Measure latency, memory traffic, power
        return {
            "latency_ms": latency,
            "memory_traffic_bytes": bytes_moved,
            "power_watts": peak_power,
            "energy_joules": energy,
            "flops_achieved": actual_flops,
            "memory_bandwidth_used": bw_used,
        }
```

**Metrics to Track**:
- `latency_ms_p95`: Kernel execution time
- `memory_traffic_bytes`: Total memory movement
- `flops_achieved`: Actual FLOP/s achieved
- `memory_bandwidth_used`: Percentage of peak BW
- `energy_joules`: Total energy for operation

**Trials**: 10 on different batch sizes and matrix dimensions

**Quality Floor**: N/A (numerical output bitwise identical)

**Latency Budget**: p95 <= 50ms for dense kernels

---

## Common Implementation Pattern

All 4 experiments follow this pattern:

```python
class ExperimentExecutor:
    def __init__(self, baseline_path, experiment_config):
        self.baseline = load_baseline(baseline_path)
        self.config = experiment_config
        self.metrics_collector = MetricsCollector()

    def run_trial(self, trial_num: int, benchmark_id: str) -> Dict[str, float]:
        """
        Execute one trial of the experiment.
        
        Returns dictionary of metrics.
        """
        try:
            # 1. Setup: Load model at baseline
            model = load_model_at_precision(self.baseline.representation_type)
            
            # 2. Mutate: Apply experimental change
            model = apply_mutation(model, self.config)
            
            # 3. Execute: Run benchmark
            results = benchmark.run(model)
            
            # 4. Measure: Collect metrics
            metrics = {
                "accuracy": results.accuracy,
                "latency_ms": results.latency,
                "energy_joules": results.energy,
                "throughput_tok_sec": results.throughput,
            }
            
            # 5. Check: Quality floor
            if metrics["accuracy"] < self.baseline.accuracy * 0.99:
                raise QualityFloorViolation()
            
            return metrics
            
        except Exception as e:
            return {"error": str(e)}

# Usage in experiment runner
runner = ExperimentRunner(baseline_mgr, benchmark_registry, metrics_collector)
executor = Experiment1Executor(baseline, config)
experiment = runner.run_experiment(
    experiment_id="exp_001",
    trial_executor=executor.run_trial,
)
```

---

## Acceptance Rules (Same for All 4)

Accept experiment ONLY if:

1. ✅ **Minimum Effect Size**: abs(effect_size) >= 0.10 (10% improvement)
2. ✅ **Quality Floor**: accuracy >= baseline × 0.99 (99% of baseline)
3. ✅ **Latency Budget**: p95_latency <= budget_ms
4. ✅ **Statistical Significance**: p-value < 0.05 (Welch's t-test)
5. ✅ **Confidence Interval**: CI excludes zero
6. ✅ **Holdout Pass**: Replicates on holdout benchmark set
7. ✅ **Complexity Cost**: Orchestration overhead < 5% of savings

---

## Metrics Collection Checklist

For each trial, measure:

- [ ] Task quality (accuracy, F1, ROUGE, etc.)
- [ ] Latency p50, p95, p99 (milliseconds)
- [ ] Throughput (tokens/sec or samples/sec)
- [ ] Energy (joules per inference) - use RAPL + GPU telemetry
- [ ] Memory traffic (bytes moved between hierarchy levels)
- [ ] Cache hit rate (if available)
- [ ] Peak power (watts)
- [ ] Compute utilization (% of peak FLOPS)

---

## Quick Checklist for Phase 2 Startup

### Prerequisites
- [ ] Baseline hardware profiled (A100, RTX 6000, etc.)
- [ ] BF16 baseline model frozen and measured
- [ ] Benchmark data prepared (ImageNet, GLUE, translation, etc.)
- [ ] Energy measurement tools configured (RAPL, GPU logging)

### Implementation
- [ ] Quantization module complete
- [ ] Sparsity module complete
- [ ] Memory optimizer complete
- [ ] Compiler fusion toolkit complete
- [ ] Trial executors written and tested
- [ ] Config files for all 4 experiments

### Execution
- [ ] Exp 1: INT4 quantization (10 trials)
- [ ] Exp 2: Token pruning (10 trials)
- [ ] Exp 3: Memory optimization (10 trials)
- [ ] Exp 4: Compiler fusion (10 trials)

### Validation
- [ ] All experiments save trial data
- [ ] All verdicts generated (accept/reject)
- [ ] Report generation working
- [ ] Holdout validation passed
- [ ] Portfolio dashboard shows all 4

### Documentation
- [ ] Individual reports generated
- [ ] Comparison report created
- [ ] Results stored in ResultsStore
- [ ] Next experiments proposed

---

## Expected Outcomes

If framework works correctly, we expect:

- **Exp 1 (Quantization)**: 12-18% ECD improvement, quality floor met
- **Exp 2 (Pruning)**: 18-25% energy reduction, some quality loss acceptable
- **Exp 3 (Memory)**: 20-35% memory traffic reduction, latency tradeoff
- **Exp 4 (Fusion)**: 12-20% latency improvement, no quality impact

These are realistic, achievable targets on existing hardware with proven techniques.

---

## After Phase 2

Once all 4 experiments complete and verdicts are stable:

1. Move to Phase 3: Mid-term experiments (RNS, LNS, posits, etc.)
2. Then Phase 4: Moonshot simulators
3. Then Phase 5: Agent-driven hypothesis generation

**Only then** introduce the hypothesis/build/skeptic agents.

The lab proves itself on known-good experiments first.
