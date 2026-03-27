# Experiment Report: exp_002_token_pruning

## Metadata

- **Hypothesis**: Dynamic token pruning improves energy efficiency >=20% with bounded quality loss.
- **Horizon**: near_term
- **Workload Class**: sparse_conditional
- **Hardware Target**: A100
- **Representation Type**: dynamic_sparsity
- **Parent Experiment**: None
- **Maturity Label**: M5
- **Verdict Source**: single_decision_engine_v1

## Mutation Scope

Permitted changes:

- pruning_strategy

## Baseline Reference

- **Baseline ID**: baseline_gpu_transformer_bf16_v1

## Benchmarks

- transformer_inference_small
- transformer_inference_medium
- transformer_inference_holdout

## Execution Timeline

- **Created**: 2026-03-27T14:02:07.493107
- **Started**: 2026-03-27T14:02:07.493107
- **Completed**: 2026-03-27T14:02:07.790749

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

- Mean: 0.9673248399572912
- Std Dev: 0.6901104635805091
- Min: 0.05218399997102097
- Max: 1.484375
- p95: 1.484375
- p99: 1.484375

#### tokens_pruned

- Mean: 103.0
- Std Dev: 0.0
- Min: 103.0
- Max: 103.0
- p95: 103.0
- p99: 103.0

#### throughput_tok_sec

- Mean: 448384.558916111
- Std Dev: 36525.18057437246
- Min: 368592.82006015035
- Max: 555163.6708314437
- p95: 483573.88640827156
- p99: 535358.6262091454

#### latency_ms

- Mean: 9.824106665473664
- Std Dev: 2.204763897554296
- Min: 5.245299995294772
- Max: 14.590999999199994
- p95: 13.27645999517699
- p99: 14.315383997891331

#### runtime_ms

- Mean: 9.824106665473664
- Std Dev: 2.204763897554296
- Min: 5.245299995294772
- Max: 14.590999999199994
- p95: 13.27645999517699
- p99: 14.315383997891331

#### ecd_improvement

- Mean: 27.452621044134656
- Std Dev: 39.18477206623309
- Min: 1.135164524463402
- Max: 135.0151586120338
- p95: 110.76407807396279
- p99: 134.87938466104205

#### power_watts

- Mean: 102.42514148116597
- Std Dev: 80.51631571419203
- Min: 8.0
- Max: 280.0
- p95: 210.78221007997186
- p99: 261.15966245358055

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
      "ecd_mean": 18.000226694003832,
      "quality_mean": 0.9377705196960835,
      "latency_p95": 14.590999999199994,
      "energy_mean": 1.061746839870466,
      "runtime_mean_ms": 9.747959998639999,
      "throughput_mean": 444288.8646340191,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.02192965420493,
      "confidence_interval": [
        2.952350015298156,
        33.694911083566396
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.04815878099451186,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "validation": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 28.077438109889698,
      "quality_mean": 0.9432356611441635,
      "latency_p95": 13.640599994687364,
      "energy_mean": 0.9231354799994733,
      "runtime_mean_ms": 10.042469998734305,
      "throughput_mean": 452536.74850797537,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 0.9305891608184984,
      "confidence_interval": [
        6.252313871963233,
        55.07281024227504
      ],
      "ci_excludes_zero": true,
      "significant": false,
      "p_value": 0.06717140564691655,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "holdout": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 36.28019832851044,
      "quality_mean": 0.9426850587333125,
      "latency_p95": 12.831399995775428,
      "energy_mean": 0.9170922000019345,
      "runtime_mean_ms": 9.681889999046689,
      "throughput_mean": 448328.06360633863,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.0652021457883645,
      "confidence_interval": [
        9.613661726729006,
        65.83631373742718
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.04110189317826701,
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
        "actual": 18.000226694003832,
        "has_data": true
      }
    },
    {
      "gate": "development_minimum_effect",
      "passed": true,
      "evidence": {
        "required": 0.1,
        "actual": 1.02192965420493,
        "has_data": true
      }
    },
    {
      "gate": "development_significance",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "p_value": 0.04815878099451186
      }
    },
    {
      "gate": "development_confidence_interval",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "ci": [
          2.952350015298156,
          33.694911083566396
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
        "validation_ecd": 28.077438109889698,
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
        "holdout_ecd": 36.28019832851044,
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
