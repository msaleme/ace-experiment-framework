# Telemetry/Variance Hardening Sprint Report

Generated: 2026-03-27T14:52:05.918556Z

Scope: exp_002_token_pruning, exp_006_token_pruning_threshold_sweep, exp_004_compiler_fusion

## 1) Measurement Dependency Map

### exp_002_token_pruning
- ECD formula: ECD improvement = ((quality_score / (runtime_ms * energy_joules)) - baseline_qat) / baseline_qat
- Upstream provenance flow: {'quality_score': 'benchmark-scored', 'runtime_ms': 'direct', 'energy_joules': 'derived', 'power_watts': 'estimated', 'baseline_qat': 'derived_from_baseline_snapshot'}
- Metric provenance classes: {'runtime_ms': 'direct', 'latency_ms': 'direct', 'throughput_tok_sec': 'direct', 'memory_peak_mb': 'direct', 'power_watts': 'estimated', 'energy_joules': 'derived', 'accuracy': 'benchmark-scored', 'accuracy_uncertainty': 'derived', 'power_watts_uncertainty': 'derived', 'energy_joules_uncertainty': 'derived', 'complexity_overhead': 'estimated', 'ecd_improvement': 'derived', 'ecd_improvement_uncertainty': 'derived', 'measurement_window_count': 'direct', 'warmup_count': 'direct', 'outlier_window_count': 'derived', 'runtime_window_std_ms': 'derived'}
- Benchmark-specific quality scoring: quality_score = candidate_accuracy * benchmark_adjustment; benchmark_adjustment = 0.985 + 0.015 * (0.70 * mean(retained_salience * salience_mass) + 0.30 * mean(context_coverage)); retained_salience = 1 - pruning_ratio * (0.55 + 0.30 * difficulty_weight); context_coverage = 1 - pruning_ratio * (0.45 + 0.20 * rare_token_density)
- Benchmark dataset inputs: [{'sample_id': 'transformer_inference_small_sample_0', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.8, 'rare_token_density': 0.060000000000000005, 'salience_mass': 0.89, 'kernel_count': 108, 'checksum_sensitivity': 0.87}, {'sample_id': 'transformer_inference_small_sample_1', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.12, 'rare_token_density': 0.060000000000000005, 'salience_mass': 0.92, 'kernel_count': 108, 'checksum_sensitivity': 0.9299999999999999}, {'sample_id': 'transformer_inference_small_sample_2', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.9400000000000001, 'rare_token_density': 0.14, 'salience_mass': 0.94, 'kernel_count': 108, 'checksum_sensitivity': 0.89}, {'sample_id': 'transformer_inference_small_sample_3', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.2000000000000002, 'rare_token_density': 0.21000000000000002, 'salience_mass': 0.96, 'kernel_count': 108, 'checksum_sensitivity': 0.9199999999999999}, {'sample_id': 'transformer_inference_small_sample_4', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.8, 'rare_token_density': 0.07, 'salience_mass': 0.92, 'kernel_count': 108, 'checksum_sensitivity': 0.87}, {'sample_id': 'transformer_inference_small_sample_5', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.0, 'rare_token_density': 0.13, 'salience_mass': 0.95, 'kernel_count': 108, 'checksum_sensitivity': 0.9}]
- Sample quality under upgraded scorer: 0.9209804075820197
- Sample energy_joules / uncertainty: 0.02 / 0.032

### exp_006_token_pruning_threshold_sweep
- ECD formula: ECD improvement = ((quality_score / (runtime_ms * energy_joules)) - baseline_qat) / baseline_qat
- Upstream provenance flow: {'quality_score': 'benchmark-scored', 'runtime_ms': 'direct', 'energy_joules': 'derived', 'power_watts': 'estimated', 'baseline_qat': 'derived_from_baseline_snapshot'}
- Metric provenance classes: {'runtime_ms': 'direct', 'latency_ms': 'direct', 'throughput_tok_sec': 'direct', 'memory_peak_mb': 'direct', 'power_watts': 'estimated', 'energy_joules': 'derived', 'accuracy': 'benchmark-scored', 'accuracy_uncertainty': 'derived', 'power_watts_uncertainty': 'derived', 'energy_joules_uncertainty': 'derived', 'complexity_overhead': 'estimated', 'ecd_improvement': 'derived', 'ecd_improvement_uncertainty': 'derived', 'measurement_window_count': 'direct', 'warmup_count': 'direct', 'outlier_window_count': 'derived', 'runtime_window_std_ms': 'derived'}
- Benchmark-specific quality scoring: quality_score = candidate_accuracy * benchmark_adjustment; benchmark_adjustment = 0.985 + 0.015 * (0.70 * mean(retained_salience * salience_mass) + 0.30 * mean(context_coverage)); retained_salience = 1 - pruning_ratio * (0.55 + 0.30 * difficulty_weight); context_coverage = 1 - pruning_ratio * (0.45 + 0.20 * rare_token_density)
- Benchmark dataset inputs: [{'sample_id': 'transformer_inference_small_sample_0', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.8, 'rare_token_density': 0.060000000000000005, 'salience_mass': 0.89, 'kernel_count': 108, 'checksum_sensitivity': 0.87}, {'sample_id': 'transformer_inference_small_sample_1', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.12, 'rare_token_density': 0.060000000000000005, 'salience_mass': 0.92, 'kernel_count': 108, 'checksum_sensitivity': 0.9299999999999999}, {'sample_id': 'transformer_inference_small_sample_2', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.9400000000000001, 'rare_token_density': 0.14, 'salience_mass': 0.94, 'kernel_count': 108, 'checksum_sensitivity': 0.89}, {'sample_id': 'transformer_inference_small_sample_3', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.2000000000000002, 'rare_token_density': 0.21000000000000002, 'salience_mass': 0.96, 'kernel_count': 108, 'checksum_sensitivity': 0.9199999999999999}, {'sample_id': 'transformer_inference_small_sample_4', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.8, 'rare_token_density': 0.07, 'salience_mass': 0.92, 'kernel_count': 108, 'checksum_sensitivity': 0.87}, {'sample_id': 'transformer_inference_small_sample_5', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.0, 'rare_token_density': 0.13, 'salience_mass': 0.95, 'kernel_count': 108, 'checksum_sensitivity': 0.9}]
- Sample quality under upgraded scorer: 0.9209804075820197
- Sample energy_joules / uncertainty: 0.02 / 0.032

### exp_004_compiler_fusion
- ECD formula: ECD improvement = ((quality_score / (runtime_ms * energy_joules)) - baseline_qat) / baseline_qat
- Upstream provenance flow: {'quality_score': 'benchmark-scored', 'runtime_ms': 'direct', 'energy_joules': 'derived', 'power_watts': 'estimated', 'baseline_qat': 'derived_from_baseline_snapshot'}
- Metric provenance classes: {'runtime_ms': 'direct', 'latency_ms': 'direct', 'throughput_tok_sec': 'direct', 'memory_peak_mb': 'direct', 'power_watts': 'estimated', 'energy_joules': 'derived', 'accuracy': 'benchmark-scored', 'accuracy_uncertainty': 'derived', 'power_watts_uncertainty': 'derived', 'energy_joules_uncertainty': 'derived', 'complexity_overhead': 'estimated', 'ecd_improvement': 'derived', 'ecd_improvement_uncertainty': 'derived', 'measurement_window_count': 'direct', 'warmup_count': 'direct', 'outlier_window_count': 'derived', 'runtime_window_std_ms': 'derived'}
- Benchmark-specific quality scoring: quality_score = candidate_accuracy * benchmark_adjustment; benchmark_adjustment = mean(1 - fusion_ratio * 0.00035 * checksum_sensitivity * log2(kernel_count + 1)) with a small launch-overhead bonus and cap in [0.995, 1.001]
- Benchmark dataset inputs: [{'sample_id': 'transformer_inference_small_sample_0', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.8, 'rare_token_density': 0.060000000000000005, 'salience_mass': 0.89, 'kernel_count': 108, 'checksum_sensitivity': 0.87}, {'sample_id': 'transformer_inference_small_sample_1', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.12, 'rare_token_density': 0.060000000000000005, 'salience_mass': 0.92, 'kernel_count': 108, 'checksum_sensitivity': 0.9299999999999999}, {'sample_id': 'transformer_inference_small_sample_2', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.9400000000000001, 'rare_token_density': 0.14, 'salience_mass': 0.94, 'kernel_count': 108, 'checksum_sensitivity': 0.89}, {'sample_id': 'transformer_inference_small_sample_3', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.2000000000000002, 'rare_token_density': 0.21000000000000002, 'salience_mass': 0.96, 'kernel_count': 108, 'checksum_sensitivity': 0.9199999999999999}, {'sample_id': 'transformer_inference_small_sample_4', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 0.8, 'rare_token_density': 0.07, 'salience_mass': 0.92, 'kernel_count': 108, 'checksum_sensitivity': 0.87}, {'sample_id': 'transformer_inference_small_sample_5', 'data_source': 'wikitext-103', 'sequence_length': 128, 'batch_size': 1, 'difficulty_weight': 1.0, 'rare_token_density': 0.13, 'salience_mass': 0.95, 'kernel_count': 108, 'checksum_sensitivity': 0.9}]
- Sample quality under upgraded scorer: 0.9822234153988216
- Sample energy_joules / uncertainty: 0.02 / 0.032

## 2) Energy Telemetry Upgrade Plan

- Direct device telemetry path implemented via ACE_DIRECT_POWER_WATTS and nvidia-smi power query when available.
- Fallback path implemented as calibrated proxy tied to measured runtime, CPU process time, benchmark batch scale, and baseline energy profile.
- Final fallback remains bounded estimate semantics with explicit uncertainty fields.
- Uncertainty metadata emitted: power_watts_uncertainty, energy_joules_uncertainty, ecd_improvement_uncertainty, energy_telemetry_mode.

## 3) Quality Metric Upgrade Plan

- Token pruning experiments now use benchmark-scored quality instead of generic accuracy reuse.
- Compiler fusion now uses benchmark-scored semantic-equivalence quality instead of flat baseline carry-forward.
- Exact protocol documentation: docs/telemetry_variance_protocol.md

## 4) Variance Reduction Protocol

- version: near_term_protocol_v2
- fixed_warmup_count: 2
- stable_measurement_windows: 5
- deterministic_seed_policy: sha256(experiment_id, benchmark_id, trial_num, window_index)
- run_isolation_policy: gc.collect + tracemalloc reset + deterministic state rebuild per window
- outlier_handling_policy: median-centered MAD filter, keep windows with |x-median| <= 3*MAD
- reset_sleep_ms: 1

## 5) Rerun Package

### exp_002_token_pruning
- ECD std before upgrade: 39.18477206623309
- upgraded_t20: trials=20, engine=rejected, skeptic=rejected, ECD std after=657.8915331843517
- Failed gates: ['holdout_independent_gate']
- Metric provenance counts (development): {'direct': 120, 'estimated': 40, 'derived': 160, 'benchmark-scored': 20, 'unknown': 0}
- Skeptic notes: ['High variance in ECD improvement suggests instability.']
- upgraded_t40: trials=40, engine=accepted, skeptic=promising_but_complex, ECD std after=677.5470096308783
- Failed gates: []
- Metric provenance counts (development): {'direct': 240, 'estimated': 80, 'derived': 320, 'benchmark-scored': 40, 'unknown': 0}
- Skeptic notes: ['High variance in ECD improvement suggests instability.']

### exp_006_token_pruning_threshold_sweep
- ECD std before upgrade: 49.72518694712725
- upgraded_t20: trials=20, engine=rejected, skeptic=rejected, ECD std after=644.861402390219
- Failed gates: ['holdout_independent_gate']
- Metric provenance counts (development): {'direct': 120, 'estimated': 40, 'derived': 160, 'benchmark-scored': 20, 'unknown': 0}
- Skeptic notes: ['High variance in ECD improvement suggests instability.']
- upgraded_t40: trials=40, engine=accepted, skeptic=promising_but_complex, ECD std after=595.3090830011938
- Failed gates: []
- Metric provenance counts (development): {'direct': 240, 'estimated': 80, 'derived': 320, 'benchmark-scored': 40, 'unknown': 0}
- Skeptic notes: ['High variance in ECD improvement suggests instability.']

### exp_004_compiler_fusion
- ECD std before upgrade: 56.784362055131346
- upgraded_t20: trials=20, engine=rejected, skeptic=rejected, ECD std after=714.9346566499556
- Failed gates: ['development_quality_floor', 'validation_transfer', 'holdout_independent_gate']
- Metric provenance counts (development): {'direct': 120, 'estimated': 40, 'derived': 160, 'benchmark-scored': 20, 'unknown': 0}
- Skeptic notes: ['High variance in ECD improvement suggests instability.']
- upgraded_t40: trials=40, engine=rejected, skeptic=rejected, ECD std after=720.8840839895512
- Failed gates: ['development_quality_floor', 'validation_transfer', 'holdout_independent_gate']
- Metric provenance counts (development): {'direct': 240, 'estimated': 80, 'derived': 320, 'benchmark-scored': 40, 'unknown': 0}
- Skeptic notes: ['High variance in ECD improvement suggests instability.']

## 6) Publication-Readiness Classification

- exp_002_token_pruning: internally credible (At 40 trials the decision engine accepts, but skeptic still downgrades due very high ECD variance and energy remains estimated.)
- exp_006_token_pruning_threshold_sweep: internally credible (At 40 trials the decision engine accepts, but skeptic still downgrades due very high ECD variance and energy remains estimated.)
- exp_004_compiler_fusion: still exploratory (Even at 40 trials the experiment fails quality-floor, validation-transfer, and holdout gates under the upgraded measurement path.)