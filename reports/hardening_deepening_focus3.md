# Hardening/Deepening Focus Report (3 Experiments)

Generated: 2026-03-27T14:14:22.290421Z

## 1) Skeptic Downgrade Analysis

### exp_002_token_pruning
- Final verdict: promising_but_complex
- Skeptic downgrade reason: SKEPTIC_RULE_HIGH_ECD_VARIANCE (ecd.std > 0.20)
- Complexity penalties applied: {'configured_max_complexity_overhead': 0.05, 'observed_complexity_overhead_mean_dev': 0.02, 'complexity_overhead_gate': {'gate': 'complexity_overhead_gate', 'passed': True, 'evidence': {'required': 0.05, 'actual': 0.02, 'samples': 10}}}
- Estimated vs direct metrics (development): {'direct': 40, 'estimated': 50, 'unknown': 0}
- Smallest change to reach accepted: Reduce ECD variance so skeptic rule does not trigger (current threshold is ecd.std <= 0.20).
- Full decision-engine gate trace:
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

### exp_004_compiler_fusion
- Final verdict: promising_but_complex
- Skeptic downgrade reason: SKEPTIC_RULE_HIGH_ECD_VARIANCE (ecd.std > 0.20)
- Complexity penalties applied: {'configured_max_complexity_overhead': 0.05, 'observed_complexity_overhead_mean_dev': 0.02, 'complexity_overhead_gate': {'gate': 'complexity_overhead_gate', 'passed': True, 'evidence': {'required': 0.05, 'actual': 0.02, 'samples': 10}}}
- Estimated vs direct metrics (development): {'direct': 40, 'estimated': 50, 'unknown': 0}
- Smallest change to reach accepted: Reduce ECD variance so skeptic rule does not trigger (current threshold is ecd.std <= 0.20).
- Full decision-engine gate trace:
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

### exp_006_token_pruning_threshold_sweep
- Final verdict: promising_but_complex
- Skeptic downgrade reason: SKEPTIC_RULE_HIGH_ECD_VARIANCE (ecd.std > 0.20)
- Complexity penalties applied: {'configured_max_complexity_overhead': 0.05, 'observed_complexity_overhead_mean_dev': 0.02, 'complexity_overhead_gate': {'gate': 'complexity_overhead_gate', 'passed': True, 'evidence': {'required': 0.05, 'actual': 0.02, 'samples': 10}}}
- Estimated vs direct metrics (development): {'direct': 40, 'estimated': 50, 'unknown': 0}
- Smallest change to reach accepted: Reduce ECD variance so skeptic rule does not trigger (current threshold is ecd.std <= 0.20).
- Full decision-engine gate trace:
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

## 2) Acceptance Recovery Plan

### exp_002_token_pruning
- Increase trial count and enforce deterministic warmup + fixed telemetry windows to reduce variance.
- Promote energy estimation to direct sampling or calibrated proxy to reduce ECD volatility.
- Retain current holdout requirement and validation transfer checks; do not relax acceptance gates.
- Only after variance reduction, rerun skeptic stage and confirm no downgrade trigger.
- Accepted scenarios in sensitivity rerun: []
- Promising scenarios in sensitivity rerun: ['trials20_t20_c0.05_holdout_default', 'trials40_t40_c0.05_holdout_default']

### exp_004_compiler_fusion
- Increase trial count and enforce deterministic warmup + fixed telemetry windows to reduce variance.
- Promote energy estimation to direct sampling or calibrated proxy to reduce ECD volatility.
- Retain current holdout requirement and validation transfer checks; do not relax acceptance gates.
- Only after variance reduction, rerun skeptic stage and confirm no downgrade trigger.
- Accepted scenarios in sensitivity rerun: []
- Promising scenarios in sensitivity rerun: ['trials20_t20_c0.05_holdout_default', 'trials40_t40_c0.05_holdout_default', 'alt_holdout_validation_t10_c0.05']

### exp_006_token_pruning_threshold_sweep
- Increase trial count and enforce deterministic warmup + fixed telemetry windows to reduce variance.
- Promote energy estimation to direct sampling or calibrated proxy to reduce ECD volatility.
- Retain current holdout requirement and validation transfer checks; do not relax acceptance gates.
- Only after variance reduction, rerun skeptic stage and confirm no downgrade trigger.
- Accepted scenarios in sensitivity rerun: []
- Promising scenarios in sensitivity rerun: ['trials20_t20_c0.05_holdout_default', 'trials40_t40_c0.05_holdout_default']

## 3) Telemetry Improvement Analysis

### exp_002_token_pruning
- Current direct metrics: ['runtime_ms', 'latency_ms', 'throughput_tok_sec', 'memory_peak_mb']
- energy_joules: Directly influences ECD; high variability propagates into skeptic variance trigger.
  - Convert to direct: Use hardware power sampling (NVML/RAPL/board telemetry) synchronized to trial window.
  - Stronger proxy: Calibrated joules model fitted to direct power traces per benchmark and batch profile.
- accuracy: Feeds quality-adjusted throughput and ECD; estimated-only path adds uncertainty.
  - Convert to direct: Run benchmark task outputs with actual scoring pipeline per split.
  - Stronger proxy: Confidence-bounded quality estimator validated against scored subsets.
- ecd_improvement: Primary skeptic signal; derived metric amplifies uncertainty from runtime and energy.
  - Convert to direct: Compute from direct quality, runtime, energy measurements only.
  - Stronger proxy: Propagate measurement uncertainty and require bounded CI width before skeptic review.

### exp_004_compiler_fusion
- Current direct metrics: ['runtime_ms', 'latency_ms', 'throughput_tok_sec', 'memory_peak_mb']
- energy_joules: Directly influences ECD; high variability propagates into skeptic variance trigger.
  - Convert to direct: Use hardware power sampling (NVML/RAPL/board telemetry) synchronized to trial window.
  - Stronger proxy: Calibrated joules model fitted to direct power traces per benchmark and batch profile.
- accuracy: Feeds quality-adjusted throughput and ECD; estimated-only path adds uncertainty.
  - Convert to direct: Run benchmark task outputs with actual scoring pipeline per split.
  - Stronger proxy: Confidence-bounded quality estimator validated against scored subsets.
- ecd_improvement: Primary skeptic signal; derived metric amplifies uncertainty from runtime and energy.
  - Convert to direct: Compute from direct quality, runtime, energy measurements only.
  - Stronger proxy: Propagate measurement uncertainty and require bounded CI width before skeptic review.

### exp_006_token_pruning_threshold_sweep
- Current direct metrics: ['runtime_ms', 'latency_ms', 'throughput_tok_sec', 'memory_peak_mb']
- energy_joules: Directly influences ECD; high variability propagates into skeptic variance trigger.
  - Convert to direct: Use hardware power sampling (NVML/RAPL/board telemetry) synchronized to trial window.
  - Stronger proxy: Calibrated joules model fitted to direct power traces per benchmark and batch profile.
- accuracy: Feeds quality-adjusted throughput and ECD; estimated-only path adds uncertainty.
  - Convert to direct: Run benchmark task outputs with actual scoring pipeline per split.
  - Stronger proxy: Confidence-bounded quality estimator validated against scored subsets.
- ecd_improvement: Primary skeptic signal; derived metric amplifies uncertainty from runtime and energy.
  - Convert to direct: Compute from direct quality, runtime, energy measurements only.
  - Stronger proxy: Propagate measurement uncertainty and require bounded CI width before skeptic review.

## 4) Sensitivity Analysis (Re-run)

### exp_002_token_pruning
- baseline_t10_c0.05_holdout_default: engine=rejected, final=rejected, dev_p=0.05374898365094497 sig=False, val_p=0.02012028392501661 sig=True, hold_p=0.05011261347115183 sig=False
- trials20_t20_c0.05_holdout_default: engine=accepted, final=promising_but_complex, dev_p=0.003021209918053113 sig=True, val_p=0.0030079640973991874 sig=True, hold_p=0.002300212257476576 sig=True
- trials40_t40_c0.05_holdout_default: engine=accepted, final=promising_but_complex, dev_p=2.7385209063047076e-05 sig=True, val_p=4.4835489587366355e-05 sig=True, hold_p=0.0012108382494853294 sig=True
- strict_complexity_t10_c0.01_holdout_default: engine=rejected, final=rejected, dev_p=0.08938887220282841 sig=False, val_p=0.02854089680472802 sig=True, hold_p=0.11545559315020697 sig=False
- loose_complexity_t10_c0.10_holdout_default: engine=rejected, final=rejected, dev_p=0.07396169926141467 sig=False, val_p=0.04557095558248942 sig=True, hold_p=0.13052576211109662 sig=False
- alt_holdout_validation_t10_c0.05: engine=rejected, final=rejected, dev_p=0.08494368446151859 sig=False, val_p=0.0510221858909203 sig=False, hold_p=0.024984110392968804 sig=True
- alt_holdout_development_t10_c0.05: engine=rejected, final=rejected, dev_p=0.05351350686945768 sig=False, val_p=0.09783618124224393 sig=False, hold_p=0.07448660241650373 sig=False

### exp_004_compiler_fusion
- baseline_t10_c0.05_holdout_default: engine=rejected, final=rejected, dev_p=0.05782347415618584 sig=False, val_p=0.042263714951425606 sig=True, hold_p=0.08176820613449268 sig=False
- trials20_t20_c0.05_holdout_default: engine=accepted, final=promising_but_complex, dev_p=0.03873254426621878 sig=True, val_p=0.004206066752442631 sig=True, hold_p=0.04012576888432371 sig=True
- trials40_t40_c0.05_holdout_default: engine=accepted, final=promising_but_complex, dev_p=0.000926740429503545 sig=True, val_p=0.0007661992967103896 sig=True, hold_p=0.0007746475713041828 sig=True
- strict_complexity_t10_c0.01_holdout_default: engine=rejected, final=rejected, dev_p=0.21367413607439825 sig=False, val_p=0.036276160919714015 sig=True, hold_p=0.07268146755640086 sig=False
- loose_complexity_t10_c0.10_holdout_default: engine=rejected, final=rejected, dev_p=0.14953205608227899 sig=False, val_p=0.0811898111302612 sig=False, hold_p=0.09773887071343508 sig=False
- alt_holdout_validation_t10_c0.05: engine=accepted, final=promising_but_complex, dev_p=0.03417142883689427 sig=True, val_p=0.035343893718670874 sig=True, hold_p=0.042510717216762375 sig=True
- alt_holdout_development_t10_c0.05: engine=rejected, final=rejected, dev_p=0.05945450776333552 sig=False, val_p=0.11827730976831177 sig=False, hold_p=0.03462774283918576 sig=True

### exp_006_token_pruning_threshold_sweep
- baseline_t10_c0.05_holdout_default: engine=rejected, final=rejected, dev_p=0.16635810137321774 sig=False, val_p=0.028396823489643556 sig=True, hold_p=0.040615620630964314 sig=True
- trials20_t20_c0.05_holdout_default: engine=accepted, final=promising_but_complex, dev_p=0.005628866418076806 sig=True, val_p=0.018580687426375656 sig=True, hold_p=0.006629592669439864 sig=True
- trials40_t40_c0.05_holdout_default: engine=accepted, final=promising_but_complex, dev_p=0.00012033917571395473 sig=True, val_p=3.108861048715748e-05 sig=True, hold_p=0.0001520215059144153 sig=True
- strict_complexity_t10_c0.01_holdout_default: engine=rejected, final=rejected, dev_p=0.1000814410003032 sig=False, val_p=0.02611731229358263 sig=True, hold_p=0.08831221899546556 sig=False
- loose_complexity_t10_c0.10_holdout_default: engine=rejected, final=rejected, dev_p=0.10356793326163453 sig=False, val_p=0.027066703207664217 sig=True, hold_p=0.027025005336079516 sig=True
- alt_holdout_validation_t10_c0.05: engine=rejected, final=rejected, dev_p=0.07935750643136853 sig=False, val_p=0.03439057898284236 sig=True, hold_p=0.039685097933708426 sig=True
- alt_holdout_development_t10_c0.05: engine=rejected, final=rejected, dev_p=0.09938511958856887 sig=False, val_p=0.03540104661575659 sig=True, hold_p=0.039760236373312274 sig=True

## 5) Final Recommendation

- exp_002_token_pruning: pursue_after_telemetry_upgrade
- exp_004_compiler_fusion: pursue_after_telemetry_upgrade
- exp_006_token_pruning_threshold_sweep: pursue_after_telemetry_upgrade