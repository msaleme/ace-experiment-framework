# Experiment Report: exp_006_token_pruning_threshold_sweep

## Metadata

- **Hypothesis**: Token pruning threshold sweep reduces energy per task by at least 20% with bounded quality loss.
- **Horizon**: near_term
- **Workload Class**: sparse_conditional
- **Hardware Target**: A100
- **Representation Type**: dynamic_pruning
- **Parent Experiment**: None
- **Maturity Label**: M5
- **Verdict Source**: single_decision_engine_v1

## Mutation Scope

Permitted changes:

- pruning_threshold

## Baseline Reference

- **Baseline ID**: baseline_gpu_transformer_bf16_v1

## Benchmarks

- transformer_inference_small
- transformer_inference_medium
- transformer_inference_holdout

## Execution Timeline

- **Created**: 2026-03-27T14:02:08.577334
- **Started**: 2026-03-27T14:02:08.577334
- **Completed**: 2026-03-27T14:02:08.883563

## Evaluation Configuration

- **Quality Floor**: 95%
- **Latency Budget (p95)**: 120.0 ms
- **Latency Budget (p99)**: 2000.0 ms
- **Minimum Effect Threshold**: 10%
- **Number of Trials**: 10
- **Confidence Level**: 95%
- **Require Holdout Pass**: True

## Results Summary

- **Verdict**: PROMISING_BUT_COMPLEX

### Summarized Metrics

#### energy_joules

- Mean: 0.9645451800024603
- Std Dev: 0.6949121500501172
- Min: 0.0477991999941878
- Max: 1.4843750000000002
- p95: 1.4843750000000002
- p99: 1.4843750000000002

#### tokens_pruned

- Mean: 103.0
- Std Dev: 0.0
- Min: 103.0
- Max: 103.0
- p95: 103.0
- p99: 103.0

#### throughput_tok_sec

- Mean: 438175.7203593997
- Std Dev: 41935.37249946613
- Min: 340793.6560441792
- Max: 492815.59211651713
- p95: 487922.12927425053
- p99: 491526.9773626003

#### latency_ms

- Mean: 10.104229999706149
- Std Dev: 2.8584406278658965
- Min: 5.974899999273475
- Max: 16.538399999262765
- p95: 15.048640001623419
- p99: 16.39461799954006

#### runtime_ms

- Mean: 10.104229999706149
- Std Dev: 2.8584406278658965
- Min: 5.974899999273475
- Max: 16.538399999262765
- p95: 15.048640001623419
- p99: 16.39461799954006

#### ecd_improvement

- Mean: 34.8446996642899
- Std Dev: 49.72518694712725
- Min: 0.9083684347079569
- Max: 161.58214442332766
- p95: 137.65329915899503
- p99: 156.43473323806572

#### power_watts

- Mean: 93.7438912188004
- Std Dev: 74.05602999339354
- Min: 8.0
- Max: 239.72464467428577
- p95: 208.30227386647874
- p99: 231.57203827857882

#### accuracy

- Mean: 0.9412304131911865
- Std Dev: 0.017487021124292082
- Min: 0.9061312488877634
- Max: 0.9729155779773241
- p95: 0.9702602559288739
- p99: 0.9724761921746012

#### memory_peak_mb

- Mean: 0.00029754638671875
- Std Dev: 0.0
- Min: 0.00029754638671875
- Max: 0.00029754638671875
- p95: 0.00029754638671875
- p99: 0.00029754638671875

#### complexity_overhead

- Mean: 0.02
- Std Dev: 0.0
- Min: 0.02
- Max: 0.02
- p95: 0.02
- p99: 0.02

### Statistical Assessment

```json
{
  "engine_version": "single_decision_engine_v1",
  "engine_only_verdict": true,
  "configured_constraints": {
    "minimum_ecd_improvement": 0.1,
    "minimum_effect_size": 0.1,
    "require_statistical_significance": true,
    "confidence_level": 0.95,
    "confidence_interval_excludes_zero": true,
    "require_holdout_pass": true,
    "require_validation_transfer": true,
    "maximum_complexity_overhead": 0.05,
    "quality_floor_relative": 0.95
  },
  "split_scores": {
    "development": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 28.653629671180894,
      "quality_mean": 0.9377705196960835,
      "latency_p95": 13.44480000261683,
      "energy_mean": 0.920067640003981,
      "runtime_mean_ms": 9.763299999031005,
      "throughput_mean": 453652.99146807624,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.1510253416124532,
      "confidence_interval": [
        8.261815687401674,
        49.848739163154605
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.030001627540103295,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "validation": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 29.128295974835325,
      "quality_mean": 0.9432356611441635,
      "latency_p95": 16.538399999262765,
      "energy_mean": 1.059788259997731,
      "runtime_mean_ms": 10.144139999465551,
      "throughput_mean": 442248.9719041051,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 0.7940197249961011,
      "confidence_interval": [
        2.641369949313109,
        61.555609437303
      ],
      "ci_excludes_zero": true,
      "significant": false,
      "p_value": 0.10955481610923673,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "holdout": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 46.75217334685347,
      "quality_mean": 0.9426850587333125,
      "latency_p95": 16.042600000218954,
      "energy_mean": 0.9137796400056687,
      "runtime_mean_ms": 10.40525000062189,
      "throughput_mean": 418625.19770601776,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.072587185210929,
      "confidence_interval": [
        14.323850221691172,
        85.83284540948517
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.04000414018128228,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    }
  },
  "gates": [
    {
      "gate": "development_minimum_ecd",
      "passed": true,
      "evidence": {
        "required": 0.1,
        "actual": 28.653629671180894,
        "has_data": true
      }
    },
    {
      "gate": "development_minimum_effect",
      "passed": true,
      "evidence": {
        "required": 0.1,
        "actual": 1.1510253416124532,
        "has_data": true
      }
    },
    {
      "gate": "development_significance",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "p_value": 0.030001627540103295
      }
    },
    {
      "gate": "development_confidence_interval",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "ci": [
          8.261815687401674,
          49.848739163154605
        ]
      }
    },
    {
      "gate": "development_quality_floor",
      "passed": true,
      "evidence": {
        "required": 0.935465,
        "quality_floor_relative": 0.95,
        "baseline_quality": 0.9847,
        "actual": 0.9377705196960835,
        "has_data": true
      }
    },
    {
      "gate": "confidence_level_configured",
      "passed": true,
      "evidence": {
        "configured": 0.95,
        "used": 0.95
      }
    },
    {
      "gate": "validation_transfer",
      "passed": true,
      "evidence": {
        "required": true,
        "validation_has_data": true,
        "validation_ecd": 29.128295974835325,
        "validation_quality": 0.9432356611441635,
        "minimum_ecd_required": 0.1,
        "quality_floor_required": 0.935465
      }
    },
    {
      "gate": "holdout_independent_gate",
      "passed": true,
      "evidence": {
        "required": true,
        "holdout_has_data": true,
        "holdout_ecd": 46.75217334685347,
        "holdout_quality": 0.9426850587333125,
        "minimum_ecd_required": 0.1,
        "quality_floor_required": 0.935465
      }
    },
    {
      "gate": "complexity_overhead_gate",
      "passed": true,
      "evidence": {
        "required": 0.05,
        "actual": 0.02,
        "samples": 10
      }
    },
    {
      "gate": "configured_constraint_coverage",
      "passed": true,
      "evidence": {
        "configured": [
          "confidence_interval_excludes_zero",
          "confidence_level",
          "maximum_complexity_overhead",
          "minimum_ecd_improvement",
          "minimum_effect_size",
          "quality_floor_relative",
          "require_holdout_pass",
          "require_statistical_significance",
          "require_validation_transfer"
        ],
        "checked": [
          "confidence_interval_excludes_zero",
          "confidence_level",
          "maximum_complexity_overhead",
          "minimum_ecd_improvement",
          "minimum_effect_size",
          "quality_floor_relative",
          "require_holdout_pass",
          "require_statistical_significance",
          "require_validation_transfer"
        ],
        "uncovered": []
      }
    }
  ],
  "constraint_coverage": {
    "configured": [
      "confidence_interval_excludes_zero",
      "confidence_level",
      "maximum_complexity_overhead",
      "minimum_ecd_improvement",
      "minimum_effect_size",
      "quality_floor_relative",
      "require_holdout_pass",
      "require_statistical_significance",
      "require_validation_transfer"
    ],
    "checked": [
      "confidence_interval_excludes_zero",
      "confidence_level",
      "maximum_complexity_overhead",
      "minimum_ecd_improvement",
      "minimum_effect_size",
      "quality_floor_relative",
      "require_holdout_pass",
      "require_statistical_significance",
      "require_validation_transfer"
    ],
    "uncovered": [],
    "all_checked": true
  },
  "final_verdict": "accepted"
}
```

## Notes

Auto-generated by full ACE closed-loop runner
Skeptic review: High variance in ECD improvement suggests instability.

## Reproducibility

- **Code Commit**: 
- **Artifact Paths**:
