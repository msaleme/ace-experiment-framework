# Skeptic Downgrade Report

Generated: 2026-03-27T14:11:36.808783Z

## exp_002_token_pruning

- Final verdict: promising_but_complex
- Verdict source: single_decision_engine_v1

### 1) Exact downgrade rule triggered
- SKEPTIC_RULE_HIGH_ECD_VARIANCE: ecd and ecd.std > 0.20 (observed_std=39.18477206623309, threshold=0.2)

### 2) Decision engine gate trace
- development_minimum_ecd: passed=True evidence={'required': 0.1, 'actual': 18.000226694003832, 'has_data': True}
- development_minimum_effect: passed=True evidence={'required': 0.1, 'actual': 1.02192965420493, 'has_data': True}
- development_significance: passed=True evidence={'required': True, 'actual': True, 'p_value': 0.04815878099451186}
- development_confidence_interval: passed=True evidence={'required': True, 'actual': True, 'ci': [2.952350015298156, 33.694911083566396]}
- development_quality_floor: passed=True evidence={'required': 0.935465, 'quality_floor_relative': 0.95, 'baseline_quality': 0.9847, 'actual': 0.9377705196960835, 'has_data': True}
- confidence_level_configured: passed=True evidence={'configured': 0.95, 'used': 0.95}
- validation_transfer: passed=True evidence={'required': True, 'validation_has_data': True, 'validation_ecd': 28.077438109889698, 'validation_quality': 0.9432356611441635, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
- holdout_independent_gate: passed=True evidence={'required': True, 'holdout_has_data': True, 'holdout_ecd': 36.28019832851044, 'holdout_quality': 0.9426850587333125, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
- complexity_overhead_gate: passed=True evidence={'required': 0.05, 'actual': 0.02, 'samples': 10}
- configured_constraint_coverage: passed=True evidence={'configured': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'checked': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'uncovered': []}

### 3) Complexity factors that caused downgrade
- ecd_std: 39.18477206623309
- ecd_mean: 27.452621044134656
- ecd_coefficient_of_variation: 1.4273599596642175
- ecd_range: 133.8799940875704
- direct_metric_count_dev: 40
- estimated_metric_count_dev: 50

### 4) Downgrade origin category
- implementation_complexity: False
- metric_uncertainty: True
- transfer_weakness: False
- reproducibility_concern: True

### 5) Minimum changes required to become accepted
- Reduce ECD variance below skeptic threshold: ecd_improvement.std <= 0.20 while preserving current decision-engine gate passes.
- Stabilize runtime and power/energy estimation path (pin execution environment; remove measurement outliers; enforce deterministic replay for telemetry workloads).
- Increase trial rigor for this experiment until variance contracts (e.g., deterministic warmup, tighter measurement windows, stricter outlier filtering policy).
- Keep holdout benchmark in declared set and maintain validation_transfer pass in decision engine.

## exp_004_compiler_fusion

- Final verdict: promising_but_complex
- Verdict source: single_decision_engine_v1

### 1) Exact downgrade rule triggered
- SKEPTIC_RULE_HIGH_ECD_VARIANCE: ecd and ecd.std > 0.20 (observed_std=56.784362055131346, threshold=0.2)

### 2) Decision engine gate trace
- development_minimum_ecd: passed=True evidence={'required': 0.1, 'actual': 30.16722116052012, 'has_data': True}
- development_minimum_effect: passed=True evidence={'required': 0.1, 'actual': 1.0959760859937653, 'has_data': True}
- development_significance: passed=True evidence={'required': True, 'actual': True, 'p_value': 0.036715917849398726}
- development_confidence_interval: passed=True evidence={'required': True, 'actual': True, 'ci': [6.1316046825417585, 52.97868268748514]}
- development_quality_floor: passed=True evidence={'required': 0.9847, 'quality_floor_relative': 1.0, 'baseline_quality': 0.9847, 'actual': 0.9847, 'has_data': True}
- confidence_level_configured: passed=True evidence={'configured': 0.95, 'used': 0.95}
- validation_transfer: passed=True evidence={'required': True, 'validation_has_data': True, 'validation_ecd': 54.99439305848118, 'validation_quality': 0.9847, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.9847}
- holdout_independent_gate: passed=True evidence={'required': True, 'holdout_has_data': True, 'holdout_ecd': 29.9007955238113, 'holdout_quality': 0.9847, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.9847}
- complexity_overhead_gate: passed=True evidence={'required': 0.05, 'actual': 0.02, 'samples': 10}
- configured_constraint_coverage: passed=True evidence={'configured': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'checked': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'uncovered': []}

### 3) Complexity factors that caused downgrade
- ecd_std: 56.784362055131346
- ecd_mean: 38.354136580937535
- ecd_coefficient_of_variation: 1.4805277114060718
- ecd_range: 171.74375915140934
- direct_metric_count_dev: 40
- estimated_metric_count_dev: 50

### 4) Downgrade origin category
- implementation_complexity: False
- metric_uncertainty: True
- transfer_weakness: False
- reproducibility_concern: True

### 5) Minimum changes required to become accepted
- Reduce ECD variance below skeptic threshold: ecd_improvement.std <= 0.20 while preserving current decision-engine gate passes.
- Stabilize runtime and power/energy estimation path (pin execution environment; remove measurement outliers; enforce deterministic replay for telemetry workloads).
- Increase trial rigor for this experiment until variance contracts (e.g., deterministic warmup, tighter measurement windows, stricter outlier filtering policy).
- Keep holdout benchmark in declared set and maintain validation_transfer pass in decision engine.

## exp_006_token_pruning_threshold_sweep

- Final verdict: promising_but_complex
- Verdict source: single_decision_engine_v1

### 1) Exact downgrade rule triggered
- SKEPTIC_RULE_HIGH_ECD_VARIANCE: ecd and ecd.std > 0.20 (observed_std=49.72518694712725, threshold=0.2)

### 2) Decision engine gate trace
- development_minimum_ecd: passed=True evidence={'required': 0.1, 'actual': 28.653629671180894, 'has_data': True}
- development_minimum_effect: passed=True evidence={'required': 0.1, 'actual': 1.1510253416124532, 'has_data': True}
- development_significance: passed=True evidence={'required': True, 'actual': True, 'p_value': 0.030001627540103295}
- development_confidence_interval: passed=True evidence={'required': True, 'actual': True, 'ci': [8.261815687401674, 49.848739163154605]}
- development_quality_floor: passed=True evidence={'required': 0.935465, 'quality_floor_relative': 0.95, 'baseline_quality': 0.9847, 'actual': 0.9377705196960835, 'has_data': True}
- confidence_level_configured: passed=True evidence={'configured': 0.95, 'used': 0.95}
- validation_transfer: passed=True evidence={'required': True, 'validation_has_data': True, 'validation_ecd': 29.128295974835325, 'validation_quality': 0.9432356611441635, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
- holdout_independent_gate: passed=True evidence={'required': True, 'holdout_has_data': True, 'holdout_ecd': 46.75217334685347, 'holdout_quality': 0.9426850587333125, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
- complexity_overhead_gate: passed=True evidence={'required': 0.05, 'actual': 0.02, 'samples': 10}
- configured_constraint_coverage: passed=True evidence={'configured': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'checked': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'uncovered': []}

### 3) Complexity factors that caused downgrade
- ecd_std: 49.72518694712725
- ecd_mean: 34.8446996642899
- ecd_coefficient_of_variation: 1.4270516728857734
- ecd_range: 160.6737759886197
- direct_metric_count_dev: 40
- estimated_metric_count_dev: 50

### 4) Downgrade origin category
- implementation_complexity: False
- metric_uncertainty: True
- transfer_weakness: False
- reproducibility_concern: True

### 5) Minimum changes required to become accepted
- Reduce ECD variance below skeptic threshold: ecd_improvement.std <= 0.20 while preserving current decision-engine gate passes.
- Stabilize runtime and power/energy estimation path (pin execution environment; remove measurement outliers; enforce deterministic replay for telemetry workloads).
- Increase trial rigor for this experiment until variance contracts (e.g., deterministic warmup, tighter measurement windows, stricter outlier filtering policy).
- Keep holdout benchmark in declared set and maintain validation_transfer pass in decision engine.
