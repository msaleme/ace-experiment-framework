# Experiment Report: exp_008_kernel_fusion_loop

## Metadata

- **Hypothesis**: Iterative kernel fusion loop reduces p95 latency by at least 10%.
- **Horizon**: near_term
- **Workload Class**: dense_linear_algebra
- **Hardware Target**: A100
- **Representation Type**: compiler_fusion
- **Parent Experiment**: None
- **Maturity Label**: M5
- **Verdict Source**: single_decision_engine_v1

## Mutation Scope

Permitted changes:

- kernel_fusion_strategy

## Baseline Reference

- **Baseline ID**: baseline_gpu_transformer_bf16_v1

## Benchmarks

- transformer_inference_small
- transformer_inference_medium
- transformer_inference_holdout

## Execution Timeline

- **Created**: 2026-03-27T14:02:09.005250
- **Started**: 2026-03-27T14:02:09.005250
- **Completed**: 2026-03-27T14:02:09.320444

## Evaluation Configuration

- **Quality Floor**: 100%
- **Latency Budget (p95)**: 120.0 ms
- **Latency Budget (p99)**: 2000.0 ms
- **Minimum Effect Threshold**: 10%
- **Number of Trials**: 10
- **Confidence Level**: 95%
- **Require Holdout Pass**: True

## Results Summary

- **Verdict**: REJECTED

### Summarized Metrics

#### energy_joules

- Mean: 0.9693973400028577
- Std Dev: 0.7911655970588346
- Min: 0.04823519999627024
- Max: 2.96875
- p95: 1.4843750000000002
- p99: 2.5382812500000016

#### throughput_tok_sec

- Mean: 435685.5918009206
- Std Dev: 62952.413146806604
- Min: 210482.41213319782
- Max: 490894.1755997382
- p95: 486474.97499765083
- p99: 489815.3605801847

#### latency_ms

- Mean: 10.355506666383008
- Std Dev: 3.40839136620285
- Min: 6.02939999953378
- Max: 20.61929999763379
- p95: 16.809585002556545
- p99: 20.222405999156763

#### runtime_ms

- Mean: 10.355506666383008
- Std Dev: 3.40839136620285
- Min: 6.02939999953378
- Max: 20.61929999763379
- p95: 16.809585002556545
- p99: 20.222405999156763

#### ecd_improvement

- Mean: 37.6420456614582
- Std Dev: 51.76954610220562
- Min: -0.2184671131182507
- Max: 163.4964849129396
- p95: 133.4819502280504
- p99: 157.94315435241666

#### power_watts

- Mean: 90.65194204463889
- Std Dev: 72.63394857576453
- Min: 8.0
- Max: 212.82582533359462
- p95: 196.41204694238826
- p99: 210.56334566356327

#### accuracy

- Mean: 0.9847
- Std Dev: 0.0
- Min: 0.9847
- Max: 0.9847
- p95: 0.9847
- p99: 0.9847

#### memory_peak_mb

- Mean: 0.00029754638671875
- Std Dev: 0.0
- Min: 0.00029754638671875
- Max: 0.00029754638671875
- p95: 0.00029754638671875
- p99: 0.00029754638671875

#### fusion_ratio

- Mean: 0.6
- Std Dev: 0.0
- Min: 0.6
- Max: 0.6
- p95: 0.6
- p99: 0.6

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
    "quality_floor_relative": 1.0
  },
  "split_scores": {
    "development": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 24.391965461294422,
      "quality_mean": 0.9847,
      "latency_p95": 20.61929999763379,
      "energy_mean": 1.0767158600094262,
      "runtime_mean_ms": 11.948520000441931,
      "throughput_mean": 394608.4812786495,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 0.9800752018253712,
      "confidence_interval": [
        4.723049575107747,
        46.54371968754762
      ],
      "ci_excludes_zero": true,
      "significant": false,
      "p_value": 0.056111524794915005,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "validation": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 48.58262732782009,
      "quality_mean": 0.9847,
      "latency_p95": 12.657599996600766,
      "energy_mean": 0.9152906799979973,
      "runtime_mean_ms": 9.47459999952116,
      "throughput_mean": 457521.6055032191,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.0243062612185623,
      "confidence_interval": [
        14.003406765135823,
        91.57569002571466
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.04774196464336614,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "holdout": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 39.95154419526007,
      "quality_mean": 0.9847,
      "latency_p95": 13.826000002154615,
      "energy_mean": 0.9161854800011497,
      "runtime_mean_ms": 9.643399999185931,
      "throughput_mean": 454926.68862089317,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.1158389785790679,
      "confidence_interval": [
        12.6595762554437,
        71.87097503390649
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.03413562793239923,
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
        "actual": 24.391965461294422,
        "has_data": true
      }
    },
    {
      "gate": "development_minimum_effect",
      "passed": true,
      "evidence": {
        "required": 0.1,
        "actual": 0.9800752018253712,
        "has_data": true
      }
    },
    {
      "gate": "development_significance",
      "passed": false,
      "evidence": {
        "required": true,
        "actual": false,
        "p_value": 0.056111524794915005
      }
    },
    {
      "gate": "development_confidence_interval",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "ci": [
          4.723049575107747,
          46.54371968754762
        ]
      }
    },
    {
      "gate": "development_quality_floor",
      "passed": true,
      "evidence": {
        "required": 0.9847,
        "quality_floor_relative": 1.0,
        "baseline_quality": 0.9847,
        "actual": 0.9847,
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
        "validation_ecd": 48.58262732782009,
        "validation_quality": 0.9847,
        "minimum_ecd_required": 0.1,
        "quality_floor_required": 0.9847
      }
    },
    {
      "gate": "holdout_independent_gate",
      "passed": true,
      "evidence": {
        "required": true,
        "holdout_has_data": true,
        "holdout_ecd": 39.95154419526007,
        "holdout_quality": 0.9847,
        "minimum_ecd_required": 0.1,
        "quality_floor_required": 0.9847
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
  "final_verdict": "rejected"
}
```

## Notes

Auto-generated by full ACE closed-loop runner
Skeptic review: High variance in ECD improvement suggests instability.

## Reproducibility

- **Code Commit**: 
- **Artifact Paths**:
