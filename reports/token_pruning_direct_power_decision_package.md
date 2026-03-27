# Token Pruning Direct-Power Decision Package

Generated: 2026-03-27T15:04:09.994547Z

Telemetry note: nvidia-smi unavailable on this host; direct stream path executed via ACE_DIRECT_POWER_WATTS override.

## Skeptic Rule Upgrade

- Old rule: ecd.std > 0.20
- New rule: (ecd.std / max(abs(ecd.mean), eps)) + (ecd_uncertainty.mean / max(abs(ecd.mean), eps)) > 0.35
- Rationale: Normalize instability by both signal magnitude and uncertainty to avoid invalid comparisons across scales while preserving strict instability detection.

## exp_002_token_pruning

- Full gate trace:
  - development_minimum_ecd: passed=True evidence={'required': 0.1, 'actual': 103.54405072095052, 'has_data': True}
  - development_minimum_effect: passed=True evidence={'required': 0.1, 'actual': 8.498192863771532, 'has_data': True}
  - development_significance: passed=True evidence={'required': True, 'actual': True, 'p_value': 1.9743742542065103e-32}
  - development_confidence_interval: passed=True evidence={'required': True, 'actual': True, 'ci': [98.56469807136465, 108.85840391148204]}
  - development_quality_floor: passed=True evidence={'required': 0.935465, 'quality_floor_relative': 0.95, 'baseline_quality': 0.9847, 'actual': 0.9398391766794287, 'has_data': True}
  - confidence_level_configured: passed=True evidence={'configured': 0.95, 'used': 0.95}
  - validation_transfer: passed=True evidence={'required': True, 'validation_has_data': True, 'validation_ecd': 2.2612152354754658, 'validation_quality': 0.9363589149986693, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
  - holdout_independent_gate: passed=False evidence={'required': True, 'holdout_has_data': True, 'holdout_ecd': -0.813836169098214, 'holdout_quality': 0.9391165522806003, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
  - complexity_overhead_gate: passed=True evidence={'required': 0.05, 'actual': 0.02, 'samples': 40}
  - configured_constraint_coverage: passed=True evidence={'configured': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'checked': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'uncovered': []}

- Power provenance: {'energy_telemetry_mode': {'direct': 320, 'estimated': 40, 'derived': 520, 'benchmark-scored': 40, 'unknown': 0}, 'direct_power_stream_override': 'ACE_DIRECT_POWER_WATTS=185.0', 'power_sample_count': 320, 'missing_data_rule': 'When nvidia-smi is unavailable, direct stream override is used; otherwise runtime-calibrated proxy fallback.'}
- ECD mean: 34.99714326244259
- ECD uncertainty mean: 1.9760906555665845
- ECD std: 49.68089135195454
- Skeptic outcome: {'suspicious': True, 'notes': ['Uncertainty-normalized instability in ECD exceeds threshold (score=1.4760, std_norm=1.4196, unc_norm=0.0565).'], 'old_rule': 'ecd.std > 0.20', 'old_rule_triggered': True, 'new_rule': '(ecd.std / max(abs(ecd.mean), eps)) + (ecd_uncertainty.mean / max(abs(ecd.mean), eps)) > 0.35', 'new_rule_triggered': True, 'instability_score': 1.476034247142599, 'normalized_std': 1.4195699054462514, 'normalized_uncertainty': 0.05646434169634751}
- Engine verdict: rejected
- Final verdict: rejected
- Final classification: internally credible

## exp_006_token_pruning_threshold_sweep

- Full gate trace:
  - development_minimum_ecd: passed=True evidence={'required': 0.1, 'actual': 99.214764357311, 'has_data': True}
  - development_minimum_effect: passed=True evidence={'required': 0.1, 'actual': 7.666821267076508, 'has_data': True}
  - development_significance: passed=True evidence={'required': True, 'actual': True, 'p_value': 9.764510486616212e-31}
  - development_confidence_interval: passed=True evidence={'required': True, 'actual': True, 'ci': [93.63911135099278, 104.8209690379653]}
  - development_quality_floor: passed=True evidence={'required': 0.935465, 'quality_floor_relative': 0.95, 'baseline_quality': 0.9847, 'actual': 0.9398391766794287, 'has_data': True}
  - confidence_level_configured: passed=True evidence={'configured': 0.95, 'used': 0.95}
  - validation_transfer: passed=True evidence={'required': True, 'validation_has_data': True, 'validation_ecd': 2.927249019615583, 'validation_quality': 0.9363589149986693, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
  - holdout_independent_gate: passed=False evidence={'required': True, 'holdout_has_data': True, 'holdout_ecd': -0.820151747414128, 'holdout_quality': 0.9391165522806003, 'minimum_ecd_required': 0.1, 'quality_floor_required': 0.935465}
  - complexity_overhead_gate: passed=True evidence={'required': 0.05, 'actual': 0.02, 'samples': 40}
  - configured_constraint_coverage: passed=True evidence={'configured': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'checked': ['confidence_interval_excludes_zero', 'confidence_level', 'maximum_complexity_overhead', 'minimum_ecd_improvement', 'minimum_effect_size', 'quality_floor_relative', 'require_holdout_pass', 'require_statistical_significance', 'require_validation_transfer'], 'uncovered': []}

- Power provenance: {'energy_telemetry_mode': {'direct': 320, 'estimated': 40, 'derived': 520, 'benchmark-scored': 40, 'unknown': 0}, 'direct_power_stream_override': 'ACE_DIRECT_POWER_WATTS=185.0', 'power_sample_count': 320, 'missing_data_rule': 'When nvidia-smi is unavailable, direct stream override is used; otherwise runtime-calibrated proxy fallback.'}
- ECD mean: 33.77395387650415
- ECD uncertainty mean: 1.908312566162618
- ECD std: 47.65958969747507
- Skeptic outcome: {'suspicious': True, 'notes': ['Uncertainty-normalized instability in ECD exceeds threshold (score=1.4676, std_norm=1.4111, unc_norm=0.0565).'], 'old_rule': 'ecd.std > 0.20', 'old_rule_triggered': True, 'new_rule': '(ecd.std / max(abs(ecd.mean), eps)) + (ecd_uncertainty.mean / max(abs(ecd.mean), eps)) > 0.35', 'new_rule_triggered': True, 'instability_score': 1.4676369383603933, 'normalized_std': 1.4111344461398958, 'normalized_uncertainty': 0.05650249222049752}
- Engine verdict: rejected
- Final verdict: rejected
- Final classification: internally credible
