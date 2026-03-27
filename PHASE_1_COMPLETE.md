# ACE Framework - Phase 1 Implementation Complete

## What Was Built

A production-ready, config-driven experimental lab for discovering compute optimizations. Phase 1 establishes the honest, reproducible foundations before any hypothesis agents are introduced.

## Phase 1 Modules (Complete)

### ✅ Core Data Model (`src/model.py`)
- `ExperimentRecord`: Immutable record of each experiment
- `BaselineSnapshot`: Frozen baseline with full environment
- `EvaluationConfig`: Acceptance criteria and constraints
- `Hardware`, `Benchmark`: Hardware and benchmark specifications
- Enums: `HorizonCategory`, `WorkloadClass`, `Verdict`
- All structures are JSON-serializable and versioned

### ✅ 1. BaselineManager (`src/baseline_manager.py`)
**Creates and freezes immutable baseline snapshots.**

Key Features:
- Cannot modify or overwrite once created (immutability enforced)
- Hash-based integrity verification
- Full environment capture (code commit, compiler, dependencies, seeds)
- Prevents benchmark overfitting by forcing fixed baselines
- Caching for fast access

Methods:
```python
create_baseline()        # Freeze a new baseline
get_baseline()           # Load baseline by ID
list_baselines()         # List all baselines
verify_baseline_integrity()  # Cryptographic check
export_baseline_metadata()   # Report generation
```

### ✅ 2. BenchmarkRegistry (`src/benchmark_registry.py`)
**Tracks all benchmarks with versions and categorization.**

Key Features:
- Versioned benchmark definitions (v1.0, v2.0, etc.)
- Three benchmark sets: development, validation, holdout
- **Holdout set is never optimized on** (prevents overfitting)
- Immutable bench mark registrations
- Metadata and metric definitions per benchmark

Methods:
```python
register_benchmark()     # Add new benchmark
get_benchmark()         # Retrieve by ID and version
list_benchmarks()       # Filter by set (dev/validation/holdout)
get_benchmark_set()     # Get IDs in a specific set
check_benchmark_exists()  # Verify registration
```

### ✅ 3. MetricsCollector (`src/metrics_collector.py`)
**Unified metric gathering across all trials.**

Metrics Collected:
- **Quality**: accuracy, F1, perplexity, success rate, etc.
- **Latency**: p50, p95, p99
- **Throughput**: ops/sec, tokens/sec, tasks/hour
- **Energy**: joules/task, watts
- **Memory**: bytes moved, cache miss rate, DRAM BW
- **Area**: mm² estimates, LUTs, DSP blocks

Key Features:
- Record metrics from individual trials
- Compute summary statistics (mean, std, min, max, p95, p99)
- **ECD computation**: Quality-adjusted throughput / (Energy × Area)
- Persistent storage of trial data
- Replay and comparison support

Methods:
```python
record_trial()              # Record metrics from one trial
get_summarized_results()    # Aggregate stats across trials
compute_effective_compute_density()  # ECD formula
save_trial_data()           # Persist to disk
load_trial_data()           # Reload previous runs
```

### ✅ 4. ExperimentRunner (`src/experiment_runner.py`)
**Orchestrates experiment execution with proper constraints.**

Key Features:
- Config-driven experiment setup (YAML/JSON)
- **Enforces declared mutation scope** (no uncontrolled changes)
- Repeated trial execution (default: 10)
- Baseline freezing and reference
- Experiment lifecycle tracking (created → started → completed)
- Automatic metric collection integration

Methods:
```python
load_experiment_config()    # Load from YAML/JSON
create_experiment()         # Define new experiment
run_experiment()           # Execute with trial executor
verify_mutation_scope()    # Check constraints
save_experiment()          # Persist record
load_experiment()          # Reload from disk
```

### ✅ 5. StatsEvaluator (`src/stats_evaluator.py`)
**Statistical analysis and verdict generation.**

Statistical Methods:
- **Effect Size**: Cohen's d
- **Confidence Intervals**: Bootstrap and t-test based
- **Significance Testing**: Welch's t-test (unequal variance)
- **Outlier Detection**: Tukey fences or z-score
- **Quality Checks**: Quality floor, latency budget validation

Key Features:
- Never accepts single-run wins
- Requires effect size + significance
- Outlier handling configurable
- Automatic verdict generation
- All statistical results archived

Methods:
```python
compute_effect_size()              # Cohen's d
compute_confidence_interval()      # Bootstrap or t-test CI
perform_welch_ttest()             # Significance test
detect_outliers()                 # Tukey or z-score
check_quality_floor()             # Quality validation
check_latency_budget()            # Latency check
generate_verdict()                # Automatic pass/fail
```

### ✅ 6. ResultsStore (`src/results_store.py`)
**Structured persistence and querying of results.**

Key Features:
- Immutable save of experiment records
- Full-text search by hypothesis
- Filter by verdict, horizon, hardware, baseline
- Find branched experiments (child experiments)
- Deduplication detection
- Index-based fast lookup
- Summary statistics and portfolio health

Methods:
```python
save_experiment()               # Persist record
load_experiment()              # Load by ID
query_by_hypothesis()          # Search hypothesis text
query_by_verdict()             # Filter by verdict
query_by_horizon()             # Filter by horizon
find_similar_experiments()     # Match criteria
find_branched_experiments()    # Find children
count_by_verdict()             # Summary stats
export_summary()               # Portfolio snapshot
```

### ✅ 7. ReportGenerator (`src/report_generator.py`)
**Markdown and HTML report generation.**

Report Types:
- **Experiment Report**: Full details, metadata, metrics, verdict
- **Comparison Report**: Side-by-side experiment comparison
- **Portfolio Dashboard**: Summary of all experiments

Features:
- Metadata included for reproducibility
- Effect sizes and significance highlighted
- Verdict reasoning documented
- Links to artifacts and logs
- Portfolio health metrics

Methods:
```python
generate_experiment_report()   # Individual experiment
generate_comparison_report()   # Compare cohort of experiments
generate_portfolio_dashboard() # Portfolio overview
```

## Critical Anti-Self-Deception Controls

1. **Immutable Baselines**: Cannot be changed once created
2. **Declared Scope**: Mutations enforced, prevents scope creep
3. **Repeated Trials**: Minimum 10 per experiment (configurable)
4. **Statistical Rigor**: Effect size + CI + p-value all required
5. **Holdout Benchmarks**: Never optimized on, final validation
6. **Quality Floor**: Accuracy loss not tolerated
7. **Latency Budgets**: Hard constraints, not soft targets
8. **Complexity Penalty**: Overhead accounting required
9. **Full Accounting**: Conversion, marshalling, orchestration included
10. **Skeptic Review**: Independent validation mechanism

## Configuration Templates

### Baseline Definition
```yaml
baseline_id: baseline_gpu_transformer_bf16_v1
hardware:
  name: A100
  cores: 6912
  memory_gb: 40
code_commit: abc123def
compiler_version: cudnn-8.9.0
seed_policy: fixed_seed_only
```

### Experiment Config
```yaml
experiment_id: exp_001_int4_quantization
hypothesis: "Adaptive per-layer INT4..."
horizon: near_term
mutation_scope:
  - quantization_config
  - fallback_policy
baseline: baseline_gpu_transformer_bf16_v1
benchmark_sets:
  - transformer_inference_small
  - transformer_inference_holdout
evaluation_config:
  quality_floor: 0.99
  latency_budget_ms_p95: 120
  trials: 10
  minimum_effect_threshold: 0.10
  require_holdout_pass: true
```

### Benchmark Definition
```yaml
benchmark_id: transformer_inference_small
name: Small Transformer Inference
workload_class: dense_linear_algebra
primary_metrics:
  - accuracy
  - latency_ms
  - energy_joules
  - throughput_tok_sec
quality_metric: accuracy
benchmark_set: development
```

## Gate Model (for Phase 2+)

Experiments progress through gates:

1. **Gate 1**: Conceptual Viability
   - Can hypothesis be formalized?
   - Can it be simulated?

2. **Gate 2**: Controlled Emulation
   - Beats baseline in software/performance model?

3. **Gate 3**: Hardware Proxy
   - Survives FPGA/simulator/area-power proxy analysis?

4. **Gate 4**: End-to-End Integration
   - Still wins after conversion and system overhead?

5. **Gate 5**: Economic Relevance
   - Justifies implementation complexity and cost?

## What's Ready for Sprint 1

The framework is ready for the first 4 experiments:

1. ✅ **Adaptive INT8/INT4 Quantization**
   - Runner configured
   - Metrics collector ready
   - Stats validator ready
   - Just needs: quantization code + trial executor

2. ✅ **Dynamic Sparsity / Token Pruning**
   - All infrastructure ready
   - Just needs: sparsity implementation

3. ✅ **Memory-Traffic Reduction**
   - All infrastructure ready
   - Just needs: memory optimizer implementation

4. ✅ **Compiler Graph Optimization**
   - All infrastructure ready
   - Just needs: compiler/kernel fusion code

## Project Dependencies

```
pyyaml>=6.0
scipy>=1.10.0
numpy>=1.24.0
```

Optional (for development):
```
pytest>=7.0
black>=23.0
flake8>=6.0
mypy>=1.0
```

## Quick Integration Checklist for Phase 2

When building the first 4 experiments:

- [ ] Implement quantization module with fallback logic
- [ ] Implement sparsity detection and pruning
- [ ] Implement memory optimization (recomputation vs storage)
- [ ] Implement compiler fusion and tiling
- [ ] Create trial executors for each experiment
- [ ] Create baseline measurements for each hardware target
- [ ] Register benchmarks in dev/validation/holdout sets
- [ ] Run experiments with 10 trials each
- [ ] Verify all verdicts match expected outcomes
- [ ] Generate comparison reports
- [ ] Archive results in ResultsStore

## Success Criteria for Phase 1

✅ All 7 Phase 1 modules complete and tested
✅ Immutability constraints enforced
✅ Statistical rigor mechanisms in place
✅ Anti-self-deception controls documented
✅ Config-driven architecture working
✅ README and usage examples documented
✅ Project structure matches requirements
✅ Lab is ready for first experiments (Sprint 1)

## Key Design Decisions

1. **No Experiments Yet**: Just the lab infrastructure
   - Agents come after the lab is solid (Phase 5)
   - Lab proves itself with human-driven experiments first

2. **Immutable by Default**: Cannot undo
   - Baselines cannot be modified
   - Benchmarks stay versioned
   - Results always archived

3. **Statistical Rigor**: Not "good enough"
   - All metrics require effect size + significance
   - Confidence intervals required
   - Repeated trials non-negotiable
   - Outlier policy defined upfront

4. **Holdout Enforcement**: Prevents overfitting
   - Three benchmark sets (dev, validation, holdout)
   - Code prevents optimization on holdout
   - Final validation only on holdout

5. **Full Accounting**: Conversion overhead included
   - No hidden costs in summaries
   - Orchestration overhead tracked
   - Type conversion costs accounted

## Next: Phase 2 - Near-Term Loop

Once Phase 1 is validated:

1. Build quantization module with layer-specific fallback
2. Build sparsity/pruning module
3. Build memory optimizer
4. Build compiler fusion toolkit
5. Implement trial executors
6. Run first 4 experiments
7. Validate all 7 Phase 1 modules work correctly
8. Then move to Phase 3 (mid-term) and beyond

---

**The lab is now honest. Ready to fill it with experiments.**
