# Boundary-Aware Evaluation Of Token Pruning Under Decision-Grade Constraints

## Authors

ACE Lab

## Date

2026-03-27

## Abstract

Optimization claims in AI systems are commonly reported as global improvements, even when they are valid only in narrow operating conditions. This work presents a decision-grade experimental framework and a focused token-pruning case study designed to identify where optimization benefits hold, where they degrade, and why. The framework enforces immutable baselines, declared mutation scope, split-aware execution across development/validation/holdout, telemetry provenance, and a single gate-based verdict engine with explicit traceability. Across two token-pruning experiments, we find a consistent bounded-efficiency regime: strong positive effective compute density (ECD) at low sequence length and batch, edge-of-viability zones at intermediate scales, and deterministic collapse beyond runtime-envelope boundaries. The dominant boundary variables are sequence length and batch size. Hidden size and model depth are non-dominant in the current implementation due to workload-path and kernel-level coupling. These results support a boundary-first deployment policy and argue against average-only optimization acceptance.

## Keywords

Token pruning, compute efficiency, boundary analysis, holdout validation, telemetry provenance, reproducible experimentation, decision engines, deployment safety

## 1. Introduction

The central practical question for optimization is not whether an optimization works on average. The central question is under which operating conditions it remains beneficial and decision-safe.

Token pruning is a useful case because it often shows large gains in small to moderate settings and ambiguous behavior at larger scales. Without split-aware controls and hard holdout gates, these mixed behaviors are easy to over-interpret.

We make the following contributions:

1. Boundary-aware evaluation method:
  We introduce a decision-grade evaluation method that enforces split-aware validation, telemetry provenance, and gate-based acceptance, enabling falsifiable determination of condition-dependent optimization validity rather than average-case reporting.
2. Empirical bounded-efficiency result:
  Across two token-pruning experiments, we show that efficiency gains are confined to a defined operating envelope (sequence length up to 256 and batch up to 4), with consistent collapse outside this region.
3. Mechanism claim:
  We demonstrate that failure is driven by runtime-envelope dynamics: the ECD denominator (runtime multiplied by energy) grows faster than pruning benefit beyond boundary conditions, yielding predictable sign inversion.
4. Deployment implication:
  We show that optimization acceptance must be condition-dependent; boundary-aware policies are required because average-case acceptance can approve optimizations that fail in holdout-relevant regimes.

## 2. Research Questions

RQ1: Does token pruning satisfy decision-grade acceptance constraints across development, validation, and independent holdout?

RQ2: What operating envelope over sequence length and batch size yields positive, near-neutral, or negative ECD?

RQ3: Which variables dominate failure boundaries, and what mechanism explains the transition from gain to collapse?

RQ4: Are failures due to transfer mismatch, measurement noise, or threshold sensitivity?

## 3. System Under Study

Core implementation modules:

- src/decision_engine.py
- src/near_term_telemetry.py
- src/benchmark_quality.py
- src/experiment_runner.py
- src/metrics_collector.py
- agents/skeptic/skeptic_agent.py

Framework controls:

- Immutable baselines and declared mutation scope.
- Split-aware scoring for development, validation, and holdout.
- Single decision engine with explicit gate trace and configured-constraint coverage checks.
- Skeptic review with uncertainty-normalized instability rule.
- Artifact-first reporting.

## 4. Experimental Design

### 4.1 Experiment Scope

Included only:

- exp_002_token_pruning
- exp_006_token_pruning_threshold_sweep

Excluded from this paper:

- all non-token-pruning families

### 4.2 Splits And Benchmarks

- Development: transformer_inference_small
- Validation: transformer_inference_medium
- Holdout: transformer_inference_holdout

Holdout benchmark remains read-only and outside optimization loops.

### 4.3 Primary Outcome

ECD improvement, where near-term telemetry records runtime and energy and quality is benchmark-scored.

From src/near_term_telemetry.py:

- candidate_qat = quality_score / (runtime_ms * energy_joules)
- baseline_qat = baseline_accuracy / (baseline_latency_ms * baseline_energy_joules)
- ecd_improvement = (candidate_qat - baseline_qat) / |baseline_qat|

### 4.4 Statistical Policy

Decision gates in src/decision_engine.py evaluate at minimum:

- minimum ECD threshold
- minimum effect size
- significance requirement
- confidence interval excludes zero
- quality floor
- validation transfer requirement
- independent holdout gate
- complexity overhead cap
- configured-constraint coverage

Split scoring uses Welch tests and confidence intervals via src/stats_evaluator.py.

### 4.4.1 Statistical Validity and Threshold Justification

The primary deployment metric is ECD improvement under multiplicative cost (runtime multiplied by energy). We use ECD thresholding for regime classification, not for claiming universal effect size precision.

Threshold justification:
- ECD at or above 0.1 is treated as minimum practical improvement because smaller gains are readily dominated by measurement variance, operational overhead, and configuration drift.
- This threshold is practical-significance aligned rather than arbitrary.

Inference policy:
- Welch-style comparisons and confidence intervals are used to avoid equal-variance assumptions across development, validation, and holdout splits.
- A configuration is accepted only when directional and uncertainty criteria are jointly satisfied by gate policy.

Power and sample-size scope:
- each configuration aggregates repeated trials with confidence interval estimation
- the study is not powered for fine-grained threshold estimation near the decision boundary
- the statistical objective is stable regime classification (sign and consistency), not precise point estimation of small-magnitude effects

Sensitivity statement:
- boundary transitions are robust to moderate threshold variation
- changing decision margins shifts a small number of edge cells but does not remove the observed positive, transition, and collapse structure of the regime map

### 4.5 Skeptic Policy

From agents/skeptic/skeptic_agent.py:

- old rule: ecd.std > 0.20
- new rule: (ecd.std / |ecd.mean|) + (ecd_uncertainty.mean / |ecd.mean|) > 0.35

The upgraded rule normalizes instability by signal magnitude and uncertainty.

### 4.6 Telemetry Protocol

From src/near_term_telemetry.py and docs/telemetry_variance_protocol.md:

- deterministic seeded windows
- warmups + stable windows
- MAD-based outlier filtering
- direct power path with fallback hierarchy
- provenance and uncertainty metadata persisted per metric

Runtime environment limitation in focused runs:

- native nvidia-smi unavailable on host
- direct power path exercised through ACE_DIRECT_POWER_WATTS override

## 5. Results

### 5.1 Split-Aware Holdout Outcomes

Both token-pruning experiments were rejected by the decision engine under unchanged standards.

From reports/holdout_transfer_diagnosis_token_pruning.json:

- exp_002 holdout:
  - holdout ECD mean = -0.8271
  - holdout quality mean = 0.9391
  - holdout gate threshold: minimum ECD >= 0.1, quality floor >= 0.935465
  - quality passes; ECD fails
- exp_006 holdout:
  - holdout ECD mean = -0.8061
  - holdout quality mean = 0.9391
  - same threshold profile
  - quality passes; ECD fails

Interpretation: failure is not due to quality-floor collapse; it is ECD transfer collapse on holdout.

### 5.2 Operating Envelope: 2D Consensus Regime

From reports/token_pruning_2d_regime_table.md:

- strong positive envelope: seq <= 256 and batch <= 4
- edge envelope: 384 x <=2, 512 x 1
- boundary cells: 128 x 6, 384 x 3, 512 x 2
- broad negative region: higher seq x batch combinations, especially seq >= 768

Cross-experiment disagreement in the tested grid is minimal:

- one adjacent-band disagreement at seq=512, batch=2

### 5.3 Breakpoint Ranges

Sequence-length breakpoints by batch:

- batch=1: positive through seq=512, negative by seq=768
- batch=2: positive through seq=384, near-neutral by seq=512
- batch=3: positive through seq=256, near-neutral by seq=384
- batch=4: positive through seq=256, negative by seq=384
- batch=6: positive through seq=64, near-neutral by seq=128

Batch-size breakpoints by sequence length:

- seq=64: positive through batch=6, negative by batch=8
- seq=128: positive through batch=4, near-neutral by batch=6
- seq=192 and seq=256: positive through batch=4, negative by batch=6
- seq=384: positive through batch=2, near-neutral by batch=3
- seq=512: positive through batch=1, near-neutral by batch=2

### 5.4 Dominant Variables And Mechanism

From reports/token_pruning_boundary_conditions.json:

- dominant boundary variable for both experiments: sequence length
- second strongest: batch
- hidden size and depth did not produce primary boundary flips in the current implementation

Mechanism-level interpretation:

- runtime increases sharply with seq x batch in the measured workload path
- energy scales with runtime in the direct-power path
- ECD denominator runtime x energy therefore grows fast enough to overtake pruning gains

This yields a structural runtime-envelope failure rather than random degradation.

## 6. Internal Validity, External Validity, And Threats

### 6.1 Internal Validity Controls

- deterministic seeding policy at measurement-window level
- split isolation and independent holdout gate
- gate trace artifacting with explicit evidence
- skeptic instability checks
- configured-constraint coverage gate

### 6.2 Threats To Internal Validity

- two studied token-pruning experiments share a common default pruning executor path; family-level behavior may be overrepresented
- synthetic boundary sweep does not fully wire hidden size and depth into measured workload cost

### 6.3 External Validity Limits

- focused runs used ACE_DIRECT_POWER_WATTS direct override due to host tooling limits

While absolute ECD magnitudes may shift under native device telemetry, the observed regime structure is expected to remain invariant under monotonic scaling of runtime and energy. Because the failure mechanism is driven by relative growth in the ECD denominator, changes in measurement source primarily affect scale, not the ordering of configurations or the location of boundary transitions. Accordingly, this work claims robustness of boundary structure, not portability of exact numeric ECD values across hardware and telemetry stacks.

### 6.4 Construct Validity Notes

- quality remains above floor on holdout while ECD becomes negative, indicating that efficiency construct failure is separable from accuracy collapse
- boundary labels are threshold-defined and reported explicitly

## 7. Reproducibility Package

Primary artifacts:

- docs/PROJECT_CLOSEOUT.md
- docs/telemetry_variance_protocol.md
- reports/holdout_transfer_diagnosis_token_pruning.json
- reports/token_pruning_boundary_conditions.json
- reports/token_pruning_2d_regime_table.md
- reports/token_pruning_decision_memo.md

Reproducibility checklist:

- baseline references fixed
- benchmark split definitions versioned
- trials and summaries persisted
- decision traces persisted with evidence
- telemetry source/provenance included per metric
- skepticism rule and rule-debug outputs archived

## Figure Specifications

Figure 1: Regime Heatmap (core result)

- axes: sequence length by batch size
- cell encoding: positive, neutral, negative classification
- explicit positive-envelope contour or outline annotation
- boundary-cell and disagreement-cell markers
- purpose: make regime structure and envelope boundary immediately visible

Figure 2: Collapse Curve

- x-axis: sequence length
- y-axis: ECD improvement
- lines: fixed batch levels (for example 1, 2, 4)
- vertical transition marker where ECD crosses 0
- optional threshold line at ECD equals 0.1
- purpose: show crossover from beneficial to non-beneficial regimes

Figure 3: Mechanism Diagram

- curves: pruning-benefit trend versus runtime-energy denominator growth
- intersection labeled as regime boundary
- caption claim: denominator growth overtakes benefit beyond boundary
- purpose: connect empirical boundary to causal systems mechanism

Optional Figure 4 (if space permits): transfer-failure panel

- comparison: validation versus holdout ECD
- purpose: show transfer degradation is efficiency-specific, not quality-floor failure

## 8. Practical Implications

Token pruning should be deployed as a bounded optimization policy, not as a global feature flag. Deployment controls should enforce envelope-aware guardrails on sequence length and batch, with boundary cells treated as high-observation or soft-block zones.

For production evaluation practice broadly, average-only claims should be replaced by condition-aware claims with explicit failure boundaries.

## 9. Conclusion

This study shows that token pruning can be useful and non-deployable at the same time, depending on operating conditions. In this framework, the observed failure mode is predictable and boundary-shaped: as runtime-envelope pressure rises with sequence length and batch, efficiency gains collapse despite acceptable quality. Decision-grade evaluation therefore requires split-aware gate policy, telemetry provenance, and boundary reporting as first-class outputs.

The key result is not that token pruning fails. The key result is that it fails predictably outside a definable safe envelope.

## Appendix A: Evidence Snapshot

Holdout gate evidence (40-trial focused diagnosis):

- exp_002 holdout ECD mean: -0.8271, quality mean: 0.9391, gate: failed
- exp_006 holdout ECD mean: -0.8061, quality mean: 0.9391, gate: failed

Consensus envelope labels:

- positive: seq <= 256 with batch <= 4
- edge: 384 x <=2, 512 x 1
- boundary: 128 x 6, 384 x 3, 512 x 2
- negative region: mostly beyond these boundaries

Single disagreement cell across two experiments in the 2D grid:

- seq=512, batch=2 (near-neutral vs negative)
