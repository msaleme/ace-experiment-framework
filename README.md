# ACE Experiment Framework

**Automated Compute Efficiency Experimental Lab**

A config-driven experimental framework for discovering computing optimizations through rigorous, reproducible research.

## Purpose

ACE is designed to execute a systematic, automated search for compute improvements across three horizons:

- **Near-term**: Software and systems optimizations on existing hardware
- **Mid-term**: Alternative numeric representations and execution models
- **Moonshot**: Analog, photonic, in-memory, and neuromorphic concepts

The framework enforces research honesty through:
- Immutable baselines
- Declared mutation scopes
- Repeated trials with statistical validation
- Holdout benchmark sets (never optimized on)
- Complexity penalties
- Reproducibility guarantees

## Core Research Question

What combinations of representation, precision, architecture, memory strategy, scheduling, and physical substrate maximize useful computation per joule and per unit silicon area while preserving task quality, latency, and reliability?

## North-Star Metric

**Effective Compute Density (ECD)** = Quality-adjusted throughput / (Energy × Area)

Improvements come from:
1. Doing fewer unnecessary operations
2. Moving less data
3. Representing information more efficiently
4. Matching computation method to workload
5. Using heterogeneous execution paths

## Project Structure

```
compute-efficiency-lab/
├── src/                          # Core framework modules
│   ├── model.py                 # Data model and structures
│   ├── baseline_manager.py      # Immutable baseline snapshots
│   ├── benchmark_registry.py    # Benchmark definitions
│   ├── metrics_collector.py     # Unified metric collection
│   ├── experiment_runner.py     # Experiment orchestration
│   ├── stats_evaluator.py       # Statistical analysis
│   ├── results_store.py         # Results persistence
│   └── report_generator.py      # Report generation
│
├── configs/                      # Configuration files
│   ├── benchmarks/              # Benchmark definitions
│   ├── hardware/                # Hardware profiles
│   └── policies/                # Acceptance policies
│
├── experiments/                  # Experiment definitions
│   ├── near_term/
│   ├── mid_term/
│   └── moonshot/
│
├── baselines/                    # Immutable baseline snapshots
├── results/                      # Experiment results (raw trials)
├── reports/                      # Generated reports
├── docs/                         # Documentation
├── notebooks/                    # Jupyter analysis notebooks
├── simulators/                   # Numeric representation simulators
└── kernels/                      # Reference implementations
```

## Phase 1: Foundation (Complete)

Core modules implemented:

### 1. **BaselineManager**
Creates and freezes immutable baseline snapshots.
- Once created, baselines cannot be modified
- Includes code commit, compiler version, dependencies, environment
- Hash verification for integrity
- Prevents benchmark overfitting

### 2. **BenchmarkRegistry**
Tracks all benchmarks with versioning.
- Development set (used for optimization)
- Validation set (used for transfer testing)
- Holdout set (never optimized on, final validation)
- Prevents benchmark substitution

### 3. **MetricsCollector**
Unified metric gathering across trials.
- Task quality metrics
- Latency (p50, p95, p99)
- Throughput
- Energy
- Memory traffic
- Area / resource estimates
- Summary statistics (mean, std, percentiles)
- ECD computation

### 4. **ExperimentRunner**
Orchestrates experiment execution.
- Config-driven experiment setup
- Constraint enforcement (mutation scope)
- Repeated trial execution
- Baseline reference freezing
- Lifecycle tracking

### 5. **StatsEvaluator**
Statistical analysis and verdicts.
- Effect size (Cohen's d)
- Confidence intervals (bootstrap and t-test based)
- Welch's t-test (doesn't assume equal variance)
- Outlier detection (Tukey fences, z-score)
- Quality floor checking
- Latency budget validation
- Automatic verdict generation

### 6. **ResultsStore**
Structured persistence and querying.
- Immutable save of all experiments
- Quick lookup by ID
- Search by hypothesis, verdict, horizon, baseline, etc.
- Index maintenance
- Summary statistics

### 7. **ReportGenerator**
Markdown and HTML report creation.
- Individual experiment reports
- Comparison cohort reports
- Portfolio dashboards
- Reproducibility metadata

## Quick Start

### Installation

```bash
pip install -e .
```

## Project Status

This repository includes the completed foundation and hardening work for the ACE research framework, plus final closeout artifacts for the token-pruning bounded-regime study.

Primary closeout references:

- `docs/PROJECT_CLOSEOUT.md`
- `reports/token_pruning_decision_memo.md`
- `reports/token_pruning_2d_regime_table.md`

### Create Your First Experiment

```python
from src import (
    BaselineManager, BenchmarkRegistry, MetricsCollector,
    ExperimentRunner, StatsEvaluator, ResultsStore, ReportGenerator,
    Hardware, Benchmark, WorkloadClass, HorizonCategory, EvaluationConfig,
)
from pathlib import Path

# Initialize managers
baseline_mgr = BaselineManager("baselines")
benchmark_registry = BenchmarkRegistry("configs/benchmarks")
metrics = MetricsCollector("results")
runner = ExperimentRunner(baseline_mgr, benchmark_registry, metrics)
stats = StatsEvaluator(metrics)
store = ResultsStore("results")
reports = ReportGenerator("reports")

# 1. Define hardware and benchmark
hardware = Hardware(
    name="A100-40GB",
    device_type="GPU",
    model="A100",
    arch="Ampere",
    cores=6912,
    memory_gb=40.0,
    peak_power_watts=300.0,
)

benchmark = Benchmark(
    benchmark_id="transformer_inference_small",
    name="Small Transformer Inference",
    workload_class=WorkloadClass.DENSE_LINEAR_ALGEBRA,
    input_size="seq_len=128, batch=1",
    primary_metrics=["accuracy", "latency_ms", "energy_joules", "throughput_tok_sec"],
    quality_metric="accuracy",
)

# 2. Create immutable baseline
baseline = baseline_mgr.create_baseline(
    baseline_id="baseline_gpu_transformer_bf16_v1",
    hardware=hardware,
    benchmark=benchmark,
    code_commit="abc123def",
    compiler_version="nvidia-cutlass-v3.2.0",
    dependency_versions={
        "torch": "2.1.0",
        "cuda": "12.1",
        "cudnn": "8.9.0",
    },
    environment={"CUDA_VISIBLE_DEVICES": "0"},
    measurement_method="pytorch_profiler + rapl",
    seed_policy="fixed_seed_only",
    notes="Baseline for transformer fp32 to int4 quantization experiments",
)

# 3. Register benchmark in appropriate set
benchmark_registry.register_benchmark(
    benchmark_id=benchmark.benchmark_id,
    name=benchmark.name,
    workload_class=benchmark.workload_class,
    input_size=benchmark.input_size,
    primary_metrics=benchmark.primary_metrics,
    benchmark_set="development",  # or "validation" or "holdout"
)

# 4. Create experiment
experiment = runner.create_experiment(
    experiment_id="exp_001_int4_quantization",
    hypothesis_text="Adaptive per-layer INT4 with BF16 fallback improves ECD on transformer inference",
    horizon_category=HorizonCategory.NEAR_TERM,
    workload_class=WorkloadClass.DENSE_LINEAR_ALGEBRA,
    hardware_target="A100",
    representation_type="mixed_precision",
    mutation_scope=["quantization_config", "fallback_policy"],
    baseline_reference=baseline.baseline_id,
    benchmark_set=["transformer_inference_small"],
    evaluation_config=EvaluationConfig(
        quality_floor=0.99,
        latency_budget_ms_p95=120.0,
        trials=10,
        minimum_effect_threshold=0.10,
        require_holdout_pass=True,
        confidence_interval_excludes_zero=True,
    ),
    notes="First experiment: quantization sweep with quality floor",
)

# 5. Run experiment with dummy executor
def dummy_trial_executor(trial_num: int, benchmark_id: str):
    """Placeholder for actual benchmark execution."""
    import random
    return {
        "accuracy": 0.98 + random.gauss(0, 0.01),
        "latency_ms": 85.0 + random.gauss(0, 5),
        "energy_joules": 0.42 + random.gauss(0, 0.05),
        "throughput_tok_sec": 185 + random.gauss(0, 10),
    }

experiment = runner.run_experiment(
    experiment_id="exp_001_int4_quantization",
    trial_executor=dummy_trial_executor,
)

# 6. Save and generate report
runner.save_experiment("exp_001_int4_quantization")
store.save_experiment(experiment)
reports.generate_experiment_report(experiment)

print(f"Experiment verdict: {experiment.verdict}")
```

## Experiment Lifecycle

### Stage 1: Hypothesis Declaration
Single sentence hypothesis with clear, testable bounds.

Example: "Adaptive per-layer INT4 with BF16 fallback improves ECD by at least 15% on transformer inference without more than 1% quality loss."

### Stage 2: Mutation Scope Definition
Explicitly declare what may change.

Example:
```yaml
mutation_scope:
  - quantization_config
  - fallback_policy
  - layer_fallback_thresholds
```

### Stage 3: Baseline Freeze
Snapshot baseline environment and measure baseline performance.

Snapshot includes:
- Code commit hash
- Compiler version
- Dependency versions (all critical libs)
- Hardware profile
- Seed policy
- Measurement method

### Stage 4: Candidate Generation
Generate experimental variants within allowed scope.

### Stage 5: Evaluation
Run benchmarks with **repeated trials** (default: 10).

### Stage 6: Statistical Review
Test significance; never accept from single run.

### Stage 7: Holdout Confirmation
Run on untouched benchmarks (holdout set).

### Stage 8: Verdict
Possible outcomes:
- **Accepted**: Repeatable gain, quality preserved, statistically significant
- **Rejected**: No meaningful gain after full accounting
- **Inconclusive**: Signal too noisy or data insufficient
- **Promising But Complex**: Interesting but engineering overhead too high
- **Interesting For Moonshot**: Worth strategic tracking

### Stage 9: Archival and Branching
Store results and generate next hypotheses.

## Statistical Acceptance Rules

Accept only if ALL conditions are met:

1. **Minimum Effect Size**: Mean improvement ≥ threshold (default: 2%)
2. **Quality Floor**: Quality ≥ baseline × quality_floor (default: 99%)
3. **Latency Budget**: p95 latency ≤ budget (configurable)
4. **Statistical Significance**: p < 0.05 (Welch's t-test)
5. **Confidence Interval**: CI excludes zero improvement
6. **Transfer**: Replicates across at least 2 benchmark categories
7. **Complexity Cost**: Final gain after overhead accounting

## Anti-Self-Deception Controls

- **Holdout Benchmarks**: Never optimize on these
- **Baseline Refresh**: Periodic re-measurement of baseline
- **Complexity Penalty**: Penalize high orchestration overhead
- **Full Accounting**: Include conversion, communication, orchestration overhead
- **Repeated Trials**: Minimum 10 per experiment
- **Outlier Handling**: Defined outlier policy (Tukey fences or z-score)
- **Skeptic Review**: Independent validation of wins
- **Conversion Overhead**: Account for type conversions, marshalling

## First 4 Experiments (Sprint 1)

Fast path to real signal on existing hardware:

1. **Adaptive INT8/INT4 Quantization**
   - Layer-specific precision fallback
   - Quality floor: 99%
   - Target: 10-20% ECD improvement

2. **Dynamic Sparsity / Token Pruning**
   - Threshold sweep for token importance
   - Target: 15-30% energy reduction
   - Quality floor: 99%

3. **Memory-Traffic Reduction**
   - Activation recomputation vs. storage tradeoff
   - Prefetch optimization
   - Target: 20-40% reduction in bytes moved

4. **Compiler Graph Optimization**
   - Kernel fusion
   - Tiling optimization
   - Operator scheduling
   - Target: 10-15% latency improvement

## Configuration Files

All experiments start from YAML/JSON configs.

### Example Experiment Config

```yaml
experiment_id: exp_000341
horizon: near_term
hypothesis: "Adaptive per-layer INT4 with BF16 fallback improves ECD on transformer inference"
baseline: baseline_gpu_transformer_bf16_v1
mutation_scope:
  - quantization_config
  - fallback_policy
hardware_target: a100
benchmark_sets:
  - transformer_inference_small
  - transformer_inference_holdout
quality_floor:
  metric: accuracy
  minimum_relative_to_baseline: 0.99
latency_budget_ms_p95: 120
trials: 10
acceptance:
  minimum_ecd_improvement: 0.10
  require_holdout_pass: true
  confidence_interval_excludes_zero: true
```

## Next Phases

### Phase 2: Near-Term Loop
- Implement quantization and sparsity modules
- Automated evaluation runner
- First 4 experiments

### Phase 3: Mid-Term Loop
- Numeric representation emulators (RNS, LNS, posits)
- FPGA and hardware proxy support
- Heterogeneous arithmetic testing

### Phase 4: Moonshot Loop
- Analog, photonic, in-memory simulators
- System-level overhead modeling
- Strategic research reports

### Phase 5: Portfolio Intelligence
- Cross-lane ranking
- Budget-aware experiment selection
- Automatic branching from promising results
- Agent-driven hypothesis generation

## Design Principles

1. **Config-driven**: Every experiment is reproducible from config
2. **Immutable baselines**: Prevents baseline drift, benchmark overfitting
3. **Repeated trials**: Statistical validity, not single-run luck
4. **Declared scope**: No uncontrolled experiments
5. **Honest accounting**: Full overhead, no hidden costs
6. **Self-aware skepticism**: Controls against false positives
7. **Portfolio view**: Not optimizing one benchmark, discovering tradeoffs
8. **Reproducibility first**: All results must be archivable and replayable

## References

- Framework design based on best practices in:
  - Automated machine learning (NAS, hyperparameter search)
  - Clinical trial methodology (randomization, blinding, statistical rigor)
  - Hardware architecture research (reproducible artifact evaluation)
  - Adversarial robustness testing (skeptic agents)

## License

MIT

## Contact

ACE Lab Team
