# ACE Validated Results

This document summarizes findings that have passed ACE's full evaluation chain: split-aware execution across development, validation, and holdout sets; repeated trials with statistical gating; skeptic review; and explicit telemetry provenance declaration.

A result is listed here only when it carries a clear thesis, a defined operating envelope, and honest caveats. Exploratory findings and inconclusive experiments are tracked in the portfolio dashboard, not here.

---

## Result 1: Token Pruning Has a Hard Failure Boundary

**Status:** Validated (boundary characterization complete)
**Experiments:** `exp_002_token_pruning`, `exp_006_token_pruning_threshold_sweep`
**Date:** 2026-03-27

### Thesis

Token pruning ECD gains are regime-bounded by sequence length and batch size. Outside the validated envelope, ECD degrades deterministically. This is a systems-boundary failure driven by runtime-envelope dynamics, not noise or measurement variance.

### Operating Envelope

| Region | Sequence Length | Batch Size | ECD Outcome |
|---|---|---|---|
| Strong positive | ≤ 256 | ≤ 4 | Consistent gain |
| Edge of viability | 384 | ≤ 2 | Marginal |
| Boundary | 128–512 | 3–6 | Mixed |
| Collapse | > 512 | > 4 | Deterministic loss |

Breakpoints by batch:

| Batch | Positive through | Collapses by |
|---|---|---|
| 1 | seq 512 | seq 768 |
| 2 | seq 384 | seq 512 |
| 3 | seq 256 | seq 384 |
| 4 | seq 256 | seq 384 |
| 6 | seq 64 | seq 128 |

### Mechanism

Failure is not caused by hidden-size scaling or layer-depth scaling. The dominant driver is runtime-envelope collapse: the ECD denominator (runtime × energy) grows faster than pruning benefit as sequence length and batch size increase. The pruning kernel contributes nearly flat gains across depth and does not materially reduce measured workload cost outside the positive envelope.

Hidden size and model depth are non-dominant boundary variables in the current implementation due to workload-path and kernel-level coupling.

### Deployment Implication

Token pruning should not be deployed with an average-ECD acceptance criterion. Rollout should be gated on explicit sequence-length and batch-size ceilings:

- **Safe for deployment:** seq ≤ 256, batch ≤ 4
- **Marginal, monitor closely:** seq 384, batch ≤ 2
- **Do not deploy without additional validation:** all other configurations

### Caveats and Honest Limits

**Telemetry provenance:** This result was produced under simulated power telemetry using the `ACE_DIRECT_POWER_WATTS=185.0` override path. Native `nvidia-smi` direct device telemetry was not available on the host used for the boundary sweep. The observed runtime-envelope boundary pattern is robust to this caveat; reversing it would require the pruning benefit to increase super-linearly with sequence length, which is not physically plausible in the current implementation.

**Shared executor path:** `exp_002` and `exp_006` currently route through the same default pruning executor path. The boundary characterization is effectively a family-level finding rather than two independent experimental confirmations.

**Hidden size and depth:** These variables are not materially wired into the measured workload path in the current implementation. Their role at the boundary is understated, not definitively absent.

### What Would Strengthen This Result

1. Run the boundary sweep on hardware with native direct device telemetry.
2. Wire hidden-size and depth more faithfully into the measured workload path.
3. Separate `exp_002` and `exp_006` into materially distinct executor configurations before claiming experiment-level independence.
4. Replicate the boundary pattern on a second optimization family to demonstrate the method generalizes.

### Supporting Artifacts

| Artifact | Location |
|---|---|
| Research paper (peer-review format) | [`docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md`](RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md) |
| Decision memo (deployment guidance) | [`reports/token_pruning_decision_memo.md`](../reports/token_pruning_decision_memo.md) |
| 2D regime table | [`reports/token_pruning_2d_regime_table.md`](../reports/token_pruning_2d_regime_table.md) |
| Holdout transfer diagnosis | [`reports/holdout_transfer_diagnosis_token_pruning.md`](../reports/holdout_transfer_diagnosis_token_pruning.md) |
| Boundary conditions report | [`reports/token_pruning_boundary_conditions.md`](../reports/token_pruning_boundary_conditions.md) |
| Telemetry variance protocol | [`docs/telemetry_variance_protocol.md`](telemetry_variance_protocol.md) |

---

## Pending Validation

The following experiment families have been run but have not produced a result that meets the threshold for inclusion here. They are tracked in the portfolio dashboard.

| Family | Status | Reason not listed |
|---|---|---|
| INT4/INT8 quantization | Exploratory results exist | Requires native hardware replication |
| Compiler kernel fusion | Exploratory results exist | Requires stronger holdout confirmation |
| Memory layout optimization | Exploratory results exist | Requires stronger holdout confirmation |
| Mid-term (RNS, LNS, posits) | Simulation-phase only | Not yet validated against hardware proxy |
| Moonshot (analog, photonic, neuromorphic) | Design-phase only | Not yet at simulation gate |

Full portfolio: [`reports/portfolio_dashboard.md`](../reports/portfolio_dashboard.md)

---

*A result earns a place in this document by surviving the full evaluation chain. Preliminary findings and exploratory results are not listed here.*
