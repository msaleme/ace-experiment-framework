# ACE Experiment Framework

**A boundary-discovery and anti-self-deception framework for AI efficiency research.**

The core value is not any individual finding. It is the capacity to tell when an optimization claim is true, false, or only conditionally true — with traceable evidence at every verdict.

---

## The Problem

Optimization claims in AI systems are routinely reported as global improvements — even when they are valid only in narrow operating conditions. Average-case benchmarks hide regime boundaries. Single-run results get promoted. Overheads get omitted. False wins compound.

The result: teams deploy optimizations that collapse under production load.

---

## What ACE Does

ACE is a systematic, closed-loop research program that searches the design space of AI compute efficiency and enforces the conditions necessary to trust what it finds.

Every experiment runs inside a fixed harness that enforces:

- **Immutable baselines** — no moving goalposts
- **Declared mutation scope** — no uncontrolled experiments
- **Split-aware execution** — development, validation, and holdout sets run independently
- **Repeated trials with statistical gating** — no single-run acceptance
- **Skeptic agent review** — adversarial challenge of every apparent win
- **Full overhead accounting** — conversion, orchestration, and complexity costs included

Each validated result is evidence of the method working. Each honest rejection is equally valuable.

---

## North-Star Metric: Effective Compute Density (ECD)

```
ECD = Quality-Adjusted Throughput / (Energy × Area)
```

ECD is most useful in situations where simpler metrics mislead — where throughput gains are achieved at hidden cost to quality or energy, or where benchmark-average improvements mask per-condition collapse. It is a tool for catching what aggregate reporting misses, not a replacement for supporting metrics.

---

## First Validated Result: Token Pruning Has a Hard Failure Boundary

Token pruning is a widely cited inference optimization. ACE's first completed boundary analysis produced a concrete deployment-risk finding.

**Thesis:** Token pruning ECD gains are regime-bounded by sequence length and batch size. Outside the validated envelope, ECD degrades deterministically. This is a systems-boundary failure, not noise.

| Region | Sequence Length | Batch Size | ECD Outcome |
|---|---|---|---|
| Strong positive | ≤ 256 | ≤ 4 | Consistent gain |
| Edge of viability | 384 | ≤ 2 | Marginal |
| Boundary | 128–512 | 3–6 | Mixed |
| Collapse | > 512 | > 4 | Deterministic loss |

**Deployment implication:** Token pruning should not be accepted or rejected on average. Rollout should be gated on sequence-length and batch-size ceilings, not aggregate ECD.

**Telemetry caveat:** This result was produced under simulated power telemetry (`ACE_DIRECT_POWER_WATTS` override). Native device telemetry would strengthen provenance but is unlikely to reverse the dominant boundary pattern.

Full analysis: [`docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md`](docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md) | Decision memo: [`docs/VALIDATED_RESULTS.md`](docs/VALIDATED_RESULTS.md)

---

## Research Portfolio

### Active Lane: Near-Term Software Optimizations

Software and systems work on existing hardware — the lane where ACE has produced validated results. Quantization, token pruning, kernel fusion, memory traffic reduction.

### Exploratory Lanes

**Mid-term** — Alternative numeric representations and execution models: residue number systems, logarithmic arithmetic, heterogeneous pipelines, FPGA proxies. These experiments are exploratory; none have produced validated results yet.

**Moonshot** — Unconventional compute substrates: analog MAC, photonic linear algebra, in-memory compute, neuromorphic temporal coding. This lane is strategically tracked, not active.

The three-horizon structure exists to prevent near-term work from cannibalizing long-cycle research. The external narrative rests on the near-term validated results until the exploratory lanes produce confirmed findings.

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
│   ├── near_term/               # Active
│   ├── mid_term/                # Exploratory
│   └── moonshot/                # Tracked
├── baselines/                   # Immutable baseline snapshots
├── results/                     # Raw trial data
├── reports/                     # Generated experiment and portfolio reports
└── docs/                        # Research papers, validated results, and protocols
    ├── VALIDATED_RESULTS.md                           ← start here
    ├── RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md
    ├── PROJECT_CLOSEOUT.md
    └── telemetry_variance_protocol.md
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

This domain is systematically vulnerable to false positives. ACE encodes institutional skepticism:

1. Holdout benchmarks are write-protected — never seen during optimization
2. Skeptic agent challenges every apparent win before acceptance
3. Complexity penalty discounts orchestration-heavy approaches
4. Full overhead accounting — no kernel-only celebrations
5. Baseline refresh checks prevent silent drift
6. All accepted results require reproducibility metadata
7. Telemetry provenance is declared and caveated in every report

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
| [`docs/VALIDATED_RESULTS.md`](docs/VALIDATED_RESULTS.md) | Validated findings with theses, caveats, and deployment implications |
| [`GETTING_STARTED.md`](GETTING_STARTED.md) | Quickstart and 7-element experiment walkthrough |
| [`docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md`](docs/RESEARCH_PAPER_TOKEN_PRUNING_BOUNDARY_ANALYSIS.md) | Token pruning boundary study (peer-review format) |
| [`docs/PROJECT_CLOSEOUT.md`](docs/PROJECT_CLOSEOUT.md) | Phase 1 and 2 closeout, known limits, recommended next work |
| [`docs/telemetry_variance_protocol.md`](docs/telemetry_variance_protocol.md) | Telemetry hardening and variance protocol |
| [`reports/token_pruning_decision_memo.md`](reports/token_pruning_decision_memo.md) | Deployment-risk memo: envelope, collapse boundaries, telemetry caveats |
| [`reports/portfolio_dashboard.md`](reports/portfolio_dashboard.md) | Full experiment portfolio summary |

---

## Design Principles

1. **Method over findings** — the framework's credibility compounds across experiments; individual results are evidence of the method working
2. **Boundary-first deployment policy** — optimizations are accepted with operating envelopes, not as universal improvements
3. **Honest accounting** — telemetry provenance, overhead costs, and result caveats are declared, not omitted
4. **Artifact-first reporting** — every verdict is backed by traceable artifacts
5. **Config-driven reproducibility** — every experiment is replayable from its config

---

## License

MIT

---

*The lab is honest. The rules are enforced.*
