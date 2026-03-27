# Token Pruning Decision Memo

Generated: 2026-03-27

## Executive Summary

Token pruning is useful only inside a bounded operating regime in the current implementation. Across both `exp_002_token_pruning` and `exp_006_token_pruning_threshold_sweep`, ECD is strongly positive at smaller sequence lengths and smaller batches, remains positive but compressed in the validation-like regime, and becomes near-neutral to negative as sequence length and batch size increase. The two experiments agree on the overall envelope and differ materially at only one boundary cell: `seq_len=512`, `batch=2`, where `exp_002` is near-neutral and `exp_006` is slightly negative.

## Supported Operating Envelope

- Safe positive region: `seq_len <= 256` with `batch <= 4`.
- Extended positive region: `seq_len=384` with `batch <= 2`, and `seq_len=512` with `batch=1`.
- Boundary region: `seq_len=128, batch=6`; `seq_len=384, batch=3`; `seq_len=512, batch=2`.
- Unsupported region: all points beyond those boundaries, especially `seq_len >= 768` at any batch and `batch >= 8` at any tested sequence length.

## Breakpoint Findings

- Primary boundary variable: sequence length.
- Secondary boundary variable: batch size.
- Positive-to-nonpositive sequence-length breakpoints by batch:
  - `batch=1`: positive through `seq_len=512`, negative by `seq_len=768`.
  - `batch=2`: positive through `seq_len=384`, near-neutral by `seq_len=512`.
  - `batch=3`: positive through `seq_len=256`, near-neutral by `seq_len=384`.
  - `batch=4`: positive through `seq_len=256`, negative by `seq_len=384`.
  - `batch=6`: positive through `seq_len=64`, near-neutral by `seq_len=128`.
- Positive-to-nonpositive batch breakpoints by sequence length:
  - `seq_len=64`: positive through `batch=6`, negative by `batch=8`.
  - `seq_len=128`: positive through `batch=4`, near-neutral by `batch=6`.
  - `seq_len=192`: positive through `batch=4`, negative by `batch=6`.
  - `seq_len=256`: positive through `batch=4`, negative by `batch=6`.
  - `seq_len=384`: positive through `batch=2`, near-neutral by `batch=3`.
  - `seq_len=512`: positive through `batch=1`, near-neutral by `batch=2`.

## Mechanism Summary

The current failure mode is not primarily hidden-size scaling or layer-depth scaling. It is a runtime-envelope collapse driven by the measurement path and the ECD formula. In the current telemetry path, ECD is computed from quality divided by `runtime_ms * energy_joules`. With the direct power override active, energy scales approximately linearly with runtime, so the denominator is effectively penalized super-linearly as runtime rises. Sequence length and batch size increase measured runtime substantially, while the pruning kernel contributes nearly flat gains across depth and does not materially wire hidden size into measured workload cost. The result is that scheduler/runtime growth overwhelms the pruning benefit at larger operating points.

## Recommendation For Deployment / Use

- Treat token pruning as a bounded optimization only.
- Allow deployment only within the positive consensus envelope.
- Do not rely on token pruning for holdout-scale or larger-scale transformer serving under the current implementation.
- If used in production-like experiments, gate rollout on sequence-length and batch ceilings rather than on average ECD alone.

## Risks And Caveats

- `exp_002` and `exp_006` currently share the same default pruning executor path, so this memo is a family-level decision rather than two meaningfully independent implementations.
- Hidden size and depth are not primary boundary variables in the current implementation because `hidden_dim` is not materially wired into the measured workload path and pruning benefit is nearly flat across depth.
- The regime map was generated under `ACE_DIRECT_POWER_WATTS=185.0`; native device telemetry would improve provenance but is unlikely to reverse the dominant sequence-length and batch-size boundary pattern by itself.