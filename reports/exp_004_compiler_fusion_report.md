# Experiment Report: exp_004_compiler_fusion

## Metadata

- **Hypothesis**: Kernel fusion reduces p95 latency by >=10% with semantic equivalence.
- **Horizon**: near_term
- **Workload Class**: dense_linear_algebra
- **Hardware Target**: A100
- **Representation Type**: compiler_graph_optimization
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

- **Created**: 2026-03-27T14:02:08.236415
- **Started**: 2026-03-27T14:02:08.236415
- **Completed**: 2026-03-27T14:02:08.537214

## Evaluation Configuration

- **Quality Floor**: 100%
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

- Mean: 0.9648003799976625
- Std Dev: 0.6946121382267058
- Min: 0.04690479999408126
- Max: 1.484375
- p95: 1.484375
- p99: 1.484375

#### throughput_tok_sec

- Mean: 431376.65704384114
- Std Dev: 54827.18449888496
- Min: 316848.7086032574
- Max: 494314.41375857446
- p95: 490276.80744575977
- p99: 493570.1281592548

#### latency_ms

- Mean: 9.928356666690282
- Std Dev: 2.495996335375986
- Min: 5.863099999260157
- Max: 14.540199998009484
- p95: 13.871895002739619
- p99: 14.414890999687486

#### runtime_ms

- Mean: 9.928356666690282
- Std Dev: 2.495996335375986
- Min: 5.863099999260157
- Max: 14.540199998009484
- p95: 13.871895002739619
- p99: 14.414890999687486

#### ecd_improvement

- Mean: 38.354136580937535
- Std Dev: 56.784362055131346
- Min: 1.2165666297351667
- Max: 172.9603257811445
- p95: 159.10206270293028
- p99: 169.80547726282734

#### power_watts

- Mean: 93.67928698306862
- Std Dev: 70.63562408441437
- Min: 8.0
- Max: 208.56458405060835
- p95: 190.7874031992946
- p99: 206.63847116374916

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
      "ecd_mean": 30.16722116052012,
      "quality_mean": 0.9847,
      "latency_p95": 12.62239999778103,
      "energy_mean": 0.9209626799973193,
      "runtime_mean_ms": 9.889579999435227,
      "throughput_mean": 414422.2193595935,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.0959760859937653,
      "confidence_interval": [
        6.1316046825417585,
        52.97868268748514
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.036715917849398726,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "validation": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 54.99439305848118,
      "quality_mean": 0.9847,
      "latency_p95": 14.108100003795698,
      "energy_mean": 0.9137787599989678,
      "runtime_mean_ms": 9.251540000695968,
      "throughput_mean": 462455.4234049992,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 1.029243504099739,
      "confidence_interval": [
        16.863905826858502,
        100.6549043244598
      ],
      "ci_excludes_zero": true,
      "significant": true,
      "p_value": 0.04688735971114105,
      "metric_source_counts": {
        "direct": 40,
        "estimated": 50,
        "unknown": 0
      }
    },
    "holdout": {
      "has_data": true,
      "trials": 10,
      "ecd_mean": 29.9007955238113,
      "quality_mean": 0.9847,
      "latency_p95": 14.540199998009484,
      "energy_mean": 1.0596596999967005,
      "runtime_mean_ms": 10.64394999993965,
      "throughput_mean": 417252.32836693065,
      "memory_peak_mean_mb": 0.00029754638671875,
      "complexity_overhead_mean": 0.02,
      "complexity_overhead_samples": 10,
      "effect_size": 0.813318346505916,
      "confidence_interval": [
        2.648694773234172,
        63.320516384242985
      ],
      "ci_excludes_zero": true,
      "significant": false,
      "p_value": 0.10232453544618629,
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
        "actual": 30.16722116052012,
        "has_data": true
      }
    },
    {
      "gate": "development_minimum_effect",
      "passed": true,
      "evidence": {
        "required": 0.1,
        "actual": 1.0959760859937653,
        "has_data": true
      }
    },
    {
      "gate": "development_significance",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "p_value": 0.036715917849398726
      }
    },
    {
      "gate": "development_confidence_interval",
      "passed": true,
      "evidence": {
        "required": true,
        "actual": true,
        "ci": [
          6.1316046825417585,
          52.97868268748514
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
        "validation_ecd": 54.99439305848118,
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
        "holdout_ecd": 29.9007955238113,
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
  "final_verdict": "accepted"
}
```

## Notes

Auto-generated by full ACE closed-loop runner
Skeptic review: High variance in ECD improvement suggests instability.

## Reproducibility

- **Code Commit**: 
- **Artifact Paths**:
