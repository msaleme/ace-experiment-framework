# Experiment Report: exp_003_int4_static_quant_sweep

## Metadata

- **Hypothesis**: INT4 static quantization sweep can improve ECD with acceptable quality floor enforcement.
- **Horizon**: near_term
- **Workload Class**: dense_linear_algebra
- **Hardware Target**: A100
- **Representation Type**: int4_static_quant
- **Parent Experiment**: None
- **Maturity Label**: M5
- **Verdict Source**: single_decision_engine_v1

## Mutation Scope

Permitted changes:

- quantization_config

## Baseline Reference

- **Baseline ID**: baseline_gpu_transformer_bf16_v1

## Benchmarks

- transformer_inference_small
- transformer_inference_medium
- transformer_inference_holdout

## Execution Timeline

- **Created**: 2026-03-27T14:02:07.835506
- **Started**: 2026-03-27T14:02:07.835506
- **Completed**: 2026-03-27T14:02:08.182110

## Evaluation Configuration

- **Quality Floor**: 98%
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

- Mean: 1.0626872733351775
- Std Dev: 0.65524215789705
- Min: 0.04603519994998351
- Max: 1.4843750000000002
- p95: 1.4843750000000002
- p99: 1.4843750000000002

#### throughput_tok_sec

- Mean: 397019.2623974975
- Std Dev: 48457.81850238311
- Min: 303539.4871478827
- Max: 497706.1036965955
- p95: 456720.81705390033
- p99: 486056.43865925336

#### latency_ms

- Mean: 11.44156666729638
- Std Dev: 2.6301696364124414
- Min: 5.754399993747938
- Max: 15.681999997468665
- p95: 15.4217349980172
- p99: 15.639108997929725

#### runtime_ms

- Mean: 11.44156666729638
- Std Dev: 2.6301696364124414
- Min: 5.754399993747938
- Max: 15.681999997468665
- p95: 15.4217349980172
- p99: 15.639108997929725

#### ecd_improvement

- Mean: 23.24261153784516
- Std Dev: 41.12911383492792
- Min: 1.003400460258263
- Max: 176.52891769005916
- p95: 98.6021313803964
- p99: 157.5298038345668

#### power_watts

- Mean: 91.36813504899898
- Std Dev: 59.38081008579565
- Min: 8.0
- Max: 170.93020575634964
- p95: 164.73604931840538
- p99: 169.16109570903353

#### memory_bandwidth_reduction

- Mean: 0.75
- Std Dev: 0.0
- Min: 0.75
- Max: 0.75
- p95: 0.75
- p99: 0.75

#### model_size_mb

- Mean: 1404.3487278761063
- Std Dev: 0.0
- Min: 1404.3487278761063
- Max: 1404.3487278761063
- p95: 1404.3487278761063
- p99: 1404.3487278761063

#### accuracy

- Mean: 0.9700736542515126
- Std Dev: 0.011881964352123853
- Min: 0.9461656031615151
- Max: 0.9915284559769305
- p95: 0.9897717620504843
- p99: 0.9912385709887727

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
    "quality_floor_relative": 0.98
  },
  "split_scores": {
    "development": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 11.656488033865417,
      "quality_mean": 0.9677205599847455,
      "latency_p95": 15.681999997468665,
      "energy_mean": 1.2044301599962637,
      "runtime_mean_ms": 12.167620000400348,
      "throughput_mean": 387932.03829261847,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 0.7722498805109027,
      "confidence_interval": [
        1.482406889822975,
        26.13919192234835
      ],
      "ci_excludes_zero": true,
      "significant": false,
      "p_value": 0.11827689079497881,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "validation": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 34.72830531500501,
      "quality_mean": 0.9714345047632298,
      "latency_p95": 15.534099999058526,
      "energy_mean": 1.05825130000012,
      "runtime_mean_ms": 11.062870000023395,
      "throughput_mean": 399469.7520388693,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 0.8024543479686352,
      "confidence_interval": [
        1.9438425080814108,
        74.33248575144522
      ],
      "ci_excludes_zero": true,
      "significant": false,
      "p_value": 0.10633830430965809,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "holdout": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 23.343041264665054,
      "quality_mean": 0.9710658980065624,
      "latency_p95": 14.830299995082896,
      "energy_mean": 0.9253803600091487,
      "runtime_mean_ms": 11.094210001465399,
      "throughput_mean": 403655.9968610046,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.069136205743173,
      "confidence_interval": [
        6.949369948935425,
        42.14081892112392
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.04051344850371159,
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
        "actual": 11.656488033865417,
        "has_data": true
      }
    },
    {
      "gate": "development_minimum_effect",
      "passed": true,
      "evidence": {
        "required": 0.1,
        "actual": 0.7722498805109027,
        "has_data": true
      }
    },
    {
      "gate": "development_significance",
      "passed": false,
      "evidence": {
        "required": true,
        "actual": false,
        "p_value": 0.11827689079497881
      }
    },
    {
      "gate": "development_confidence_interval",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "ci": [
          1.482406889822975,
          26.13919192234835
        ]
      }
    },
    {
      "gate": "development_quality_floor",
      "passed": true,
      "evidence": {
        "required": 0.965006,
        "quality_floor_relative": 0.98,
        "baseline_quality": 0.9847,
        "actual": 0.9677205599847455,
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
        "validation_ecd": 34.72830531500501,
        "validation_quality": 0.9714345047632298,
        "minimum_ecd_required": 0.1,
        "quality_floor_required": 0.965006
      }
    },
    {
      "gate": "holdout_independent_gate",
      "passed": true,
      "evidence": {
        "required": true,
        "holdout_has_data": true,
        "holdout_ecd": 23.343041264665054,
        "holdout_quality": 0.9710658980065624,
        "minimum_ecd_required": 0.1,
        "quality_floor_required": 0.965006
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
