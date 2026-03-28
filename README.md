# ACE Experiment Framework

**Automated Compute Efficiency Lab — A decision-grade research framework for discovering where AI compute efficiency is real, and where it isn't.**

---

## The Problem

Optimization claims in AI systems are routinely reported as global improvements — even when they are valid only in narrow operating conditions. Average-case benchmarks hide regime boundaries. Single-run results get promoted. Overheads get omitted. False wins compound.

The result: teams deploy optimizations that collapse under production load.

---

## What ACE Does

ACE is a systematic, closed-loop research program that searches the design space of AI compute efficiency — across precision, sparsity, scheduling, memory strategy, and physical substrate — and enforces the conditions necessary to trust what it finds.

Every experiment runs inside a fixed harness that enforces:

- **Immutable baselines** — no moving goalposts
- **Declared mutation scope** — no uncontrolled experiments
- **Split-aware execution** — development, validation, and holdout sets run independently
- **Repeated trials with statistical gating** — no single-run acceptance
- **Skeptic agent review** — adversarial challenge of every apparent win
- **Full overhead accounting** — conversion, orchestration, and complexity costs included

The result is a **compute discovery engine** that produces falsifiable, condition-specific answers rather than average-case claims.

---

## North-Star Metric: Effective Compute Density (ECD)

```
ECD = Quality-Adjusted Throughput / (Energy × Area)
```

ECD improves when a system does more useful work, uses less energy, or achieves the same result with less silicon-equivalent footprint — without degrading task quality.

This single composite metric enables fair comparison across near-term software optimizations, mid-term architectural alternatives, and moonshot compute substrates.

---

## Key Finding: Token Pruning Bounded-Efficiency Regime

The first completed study — a boundary-aware analysis of token pruning — produced a concrete, deployable result:

| Region | Sequence Length | Batch Size | ECD Outcome |
|---|---|---|---|
| Strong positive | ≤ 256 | ≤ 4 | Consistent gain |
| Edge of viability | 384 | ≤ 2 | Marginal |
| Boundary | 128–512 | 3–6 | Mixed |
| Collapse | > 512 | > 4 | Deterministic loss |

**Implication:** Token pruning should not be accepted or rejected on average. It should be deployed with explicit operating envelope enforcement.

Full analysis: [`docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md`](docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md)

---

## Three-Horizon Research Portfolio

### Near-Term (30–90 days)
Software and systems optimizations on existing hardware. Quantization, token pruning, kernel fusion, memory traffic reduction.

### Mid-Term
Alternative numeric representations and execution models. Residue number systems, logarithmic arithmetic, heterogeneous pipelines, FPGA proxies.

### Moonshot
Unconventional compute substrates. Analog MAC, photonic linear algebra, in-memory compute, neuromorphic temporal coding.

---

## Repository Structure

```
ace-experiment-framework/
├── src/                         # Core framework modules
│   ├── decision_engine.py       # Single verdict source with explicit gate traces
│   ├── near_term_telemetry.py   # Runtime, power, and energy provenance
│   ├── benchmark_quality.py     # Benchmark-specific quality scoring
│   ├── experiment_runner.py     # Config-driven split-aware orchestration
│   ├── stats_evaluator.py       # Effect size, confidence intervals, significance
│   ├── baseline_manager.py      # Immutable baseline snapshots and integrity checks
│   ├── benchmark_registry.py    # Dev / validation / holdout separation
│   ├── metrics_collector.py     # Unified trial and split metrics with provenance
│   ├── results_store.py         # Queryable result persistence
│   └── report_generator.py      # Markdown and HTML reporting
├── agents/
│   ├── skeptic/                 # Adversarial win challenger
│   └── build/                   # Experiment wiring and executors
├── configs/                     # Benchmark, hardware, and policy configs
├── experiments/                 # Experiment definitions by horizon
│   ├── near_term/
│   ├── mid_term/
│   └── moonshot/
├── baselines/                   # Immutable baseline snapshots
├── results/                     # Raw trial data
├── reports/                     # Generated experiment and portfolio reports
├── docs/                        # Research papers and protocols
│   ├── RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md
│   ├── PROJECT_CLOSEOUT.md
│   └── telemetry_variance_protocol.md
└── kernels/                     # Reference kernel implementations
```

---

## Verdict System

Every experiment produces one of five verdicts — automatically, from pre-declared rules:

| Verdict | Meaning |
|---|---|
| `ACCEPTED` | Repeatable gain, quality preserved, holdout confirmed |
| `REJECTED` | No meaningful gain after full overhead accounting |
| `INCONCLUSIVE` | Signal too noisy or benchmark set too narrow |
| `PROMISING_BUT_COMPLEX` | Gain exists but engineering overhead is too high |
| `INTERESTING_FOR_MOONSHOT` | Not product-ready; worth strategic tracking |

All gates are explicit and traceable. No subjective pass decisions.

---

## Anti-Self-Deception Controls

This domain is vulnerable to false positives. ACE encodes institutional skepticism:

1. Holdout benchmarks are write-protected — never seen during optimization
2. Skeptic agent challenges every apparent win before acceptance
3. Complexity penalty discounts orchestration-heavy approaches
4. Full overhead accounting — no kernel-only celebrations
5. Baseline refresh checks prevent silent drift
6. All accepted results include reproducibility metadata

---

## Quickstart

```bash
pip install -e .
python demo_run_experiment.py
```

See [`GETTING_STARTED.md`](GETTING_STARTED.md) for the full seven-element experiment walkthrough.

---

## Documentation

| Document | Purpose |
|---|---|
| [`GETTING_STARTED.md`](GETTING_STARTED.md) | Quickstart and 7-element experiment walkthrough |
| [`docs/PROJECT_CLOSEOUT.md`](docs/PROJECT_CLOSEOUT.md) | Phase 1 and 2 closeout, findings, known limits |
| [`docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md`](docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md) | Token pruning boundary study (peer-review format) |
| [`docs/telemetry_variance_protocol.md`](docs/telemetry_variance_protocol.md) | Telemetry hardening and variance protocol |
| [`reports/portfolio_dashboard.md`](reports/portfolio_dashboard.md) | Full experiment portfolio summary |
| [`reports/token_pruning_decision_memo.md`](reports/token_pruning_decision_memo.md) | Deployment guidance: token pruning operating envelope |

---

## Design Principles

1. **Boundary-first deployment policy** — optimizations are accepted with operating envelopes, not as universal improvements
2. **Artifact-first reporting** — every verdict is backed by traceable artifacts
3. **Config-driven reproducibility** — every experiment is replayable from its config
4. **Declared scope** — mutations are bounded before execution begins
5. **Portfolio view** — no single-benchmark optimization; cross-workload transferability required

---

## License

MIT

---

*The lab is honest. The rules are enforced.*
