# Telemetry And Variance Hardening Protocol

## Scope

This protocol applies to:

- exp_002_token_pruning
- exp_006_token_pruning_threshold_sweep
- exp_004_compiler_fusion

## Measurement Protocol

- Protocol version: near_term_protocol_v2
- Fixed warmup count: 2 minimum, upgraded to benchmark warmup count when benchmark metadata requires more
- Stable measurement windows: 5 minimum, upgraded to benchmark repetition count when benchmark metadata requires more
- Deterministic seed policy: sha256(experiment_id, benchmark_id, trial_num, window_index)
- Run isolation/reset policy: garbage collection, tracemalloc reset, deterministic state rebuild, short reset sleep before each measured window
- Stable measurement window aggregation: mean over filtered windows after warmups
- Outlier handling policy: median-centered MAD filter with threshold 3 * MAD

## Energy Telemetry Priority Order

1. Direct device telemetry
   - Environment override: ACE_DIRECT_POWER_WATTS
   - Command probe: nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits
2. Calibrated proxy tied to measured runtime and device state
   - Uses measured runtime, CPU process time, benchmark batch scale, baseline peak power, and calibration factor
3. Benchmark-specific bounded estimate
   - Returned as estimated power with explicit uncertainty when direct telemetry is unavailable

## Energy Uncertainty Metadata

- power_watts_uncertainty
- energy_joules_uncertainty
- energy_telemetry_mode

## Quality Scoring

### Token Pruning Experiments

- Scoring is benchmark-scored, not generic accuracy reuse
- Dataset inputs come from benchmark metadata and canonical sample suite derived from benchmark_id, data_source, input_size
- Score components:
  - retained salience
  - context coverage
- Formula:
  - quality_score = baseline_accuracy * (0.70 * mean(retained_salience * salience_mass) + 0.30 * mean(context_coverage))

### Compiler Fusion Experiment

- Scoring is benchmark-scored semantic equivalence
- Dataset inputs come from benchmark metadata and canonical checksum-sensitive sample suite
- Formula:
  - quality_score = baseline_accuracy * mean(1 - fusion_ratio * 0.0025 * checksum_sensitivity * log2(kernel_count + 1))

## Provenance Classes

- direct: measured directly from runtime execution or device telemetry
- estimated: model-based value without direct sensor confirmation
- derived: computed from other measured or estimated values
- benchmark-scored: produced by benchmark-specific scoring function over canonical dataset inputs

## Per-Split Summaries

Each split records repeated-run summaries for:

- runtime_ms
- latency_ms
- throughput_tok_sec
- memory_peak_mb
- power_watts
- energy_joules
- accuracy
- ecd_improvement
- complexity_overhead

Each split also records provenance counts and significance outputs used by the decision engine.