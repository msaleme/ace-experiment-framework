# Token Pruning 2D Regime Table And Consensus Chart

Generated: 2026-03-27

Legend:

- `P` = positive ECD (`ecd_mean > 0.10`)
- `N` = near-neutral ECD (`-0.10 <= ecd_mean <= 0.10`)
- `X` = negative ECD (`ecd_mean < -0.10`)

Consensus rule:

- If both experiments agree, use that regime.
- If they disagree by one adjacent band, classify the cell as `N`.

## Consensus Envelope

| Seq \ Batch | 1 | 2 | 3 | 4 | 6 | 8 |
| --- | --- | --- | --- | --- | --- | --- |
| 64 | P | P | P | P | P | X |
| 128 | P | P | P | P | N | X |
| 192 | P | P | P | P | X | X |
| 256 | P | P | P | P | X | X |
| 384 | P | P | N | X | X | X |
| 512 | P | N | X | X | X | X |
| 768 | X | X | X | X | X | X |
| 1024 | X | X | X | X | X | X |

## Deployment-Style Chart

```text
Batch ->      1   2   3   4   6   8
Seq 64      [P] [P] [P] [P] [P] [X]
Seq 128     [P] [P] [P] [P] [N] [X]
Seq 192     [P] [P] [P] [P] [X] [X]
Seq 256     [P] [P] [P] [P] [X] [X]
Seq 384     [P] [P] [N] [X] [X] [X]
Seq 512     [P] [N] [X] [X] [X] [X]
Seq 768     [X] [X] [X] [X] [X] [X]
Seq 1024    [X] [X] [X] [X] [X] [X]
```

## Exact Breakpoint Ranges

Sequence-length breakpoints by batch:

- `batch=1`: positive through `seq_len=512`; flips to negative in `512 < seq_len <= 768`.
- `batch=2`: positive through `seq_len=384`; flips to near-neutral in `384 < seq_len <= 512`.
- `batch=3`: positive through `seq_len=256`; flips to near-neutral in `256 < seq_len <= 384`.
- `batch=4`: positive through `seq_len=256`; flips to negative in `256 < seq_len <= 384`.
- `batch=6`: positive through `seq_len=64`; flips to near-neutral in `64 < seq_len <= 128`.
- `batch=8`: already negative by `seq_len=64`.

Batch-size breakpoints by sequence length:

- `seq_len=64`: positive through `batch=6`; flips to negative in `6 < batch <= 8`.
- `seq_len=128`: positive through `batch=4`; flips to near-neutral in `4 < batch <= 6`.
- `seq_len=192`: positive through `batch=4`; flips to negative in `4 < batch <= 6`.
- `seq_len=256`: positive through `batch=4`; flips to negative in `4 < batch <= 6`.
- `seq_len=384`: positive through `batch=2`; flips to near-neutral in `2 < batch <= 3`.
- `seq_len=512`: positive through `batch=1`; flips to near-neutral in `1 < batch <= 2`.
- `seq_len>=768`: negative for every tested batch.

## Cross-Experiment Agreement

- Overall agreement is very high.
- Only one disagreement exists in the tested 2D grid:
  - `seq_len=512`, `batch=2`
  - `exp_002`: near-neutral (`ecd_mean=-0.0737`)
  - `exp_006`: negative (`ecd_mean=-0.1261`)
  - Consensus classification: `N`

## Why Hidden Size And Depth Are Not Primary Boundary Variables

- Hidden size is not a primary boundary variable in the current implementation because the measured workload path does not materially scale work or memory with `hidden_dim`; the 2D runtime boundary is driven mostly by `seq_len` and `batch`.
- Depth is not a primary boundary variable because the pruning kernel keeps pruning benefit nearly flat across layer count via an almost constant effective pruning ratio and latency-improvement term.
- In short, the present implementation exposes runtime-envelope boundaries, not true hidden-size or depth scalability boundaries.

## Consensus Interpretation

- Supported positive envelope: all `P` cells.
- Cautionary envelope: all `N` cells.
- Unsupported envelope: all `X` cells.
- Practical deployment rule: keep token pruning at or below `seq_len=256, batch=4` for strong positive margin; treat `seq_len=384, batch<=2` and `seq_len=512, batch=1` as edge-of-envelope cases requiring additional validation.