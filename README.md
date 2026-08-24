# ACE Experiment Framework

**A boundary-discovery and anti-self-deception framework for AI efficiency research.**

**ACE makes an optimization claim earn its evidence before it earns a chart.**

## Start here

If you have an optimization result you want to trust, start with
[`docs/USING_ACE.md`](docs/USING_ACE.md). It explains the three commands, who benefits, how to read
a preflight, and what ACE does not claim.

## Reference application: Token-Bleed R5

ACE's first public claim-scoped reference application is the
[Token-Bleed R5 result](https://github.com/msaleme/token-bleed-benchmark/releases/tag/r5-results-2026-08-17).
The benchmark runner collected and scored the workload. ACE checked the frozen contract and
retained evidence, then kept the generic and claim-specific decisions separate: governed context
was accepted against raw full context, while its value and routing-miss claims against the cheap
lexical baseline were rejected under the preregistered cost rule.

That is the intended workflow: a valid narrow finding survives, but it cannot be promoted as a
broader win. See [`docs/REFERENCE_APPLICATION_TOKEN_BLEED_R5.md`](docs/REFERENCE_APPLICATION_TOKEN_BLEED_R5.md).

## Public reading path

- **Method note:** [Before the Benchmark: Make the Claimed Win Reviewable](https://pubpoint.com/publications/before-the-benchmark/)
- **Reference application:** [Token-Bleed R5 immutable release](https://github.com/msaleme/token-bleed-benchmark/releases/tag/r5-results-2026-08-17)
- **Research context:** [PubPoint Research Map](https://pubpoint.com/research-map/)

ACE is the assessment layer in this path. It evaluates retained evidence against the declared
contract; it does not create workload measurements, attest to private collection, or promote a
model-scoped result into a general deployment claim.

## Who ACE helps

ACE helps the engineer who has a promising optimization but needs to know whether it is safe to
act on, the research lead who needs a reviewable decision record, and the platform team that wants
to stop a one-off benchmark from becoming an overbroad production claim.

In a few minutes, ACE turns an experiment YAML into three useful things:

- A preflight that names missing seeds, telemetry provenance, and the exact work required before measurement.
- A provenance-bearing, overwrite-protected run record that binds the baseline, split plan, rules, runtime, and config digest.
- A plain-language claim boundary so a reviewer can distinguish “ready to measure” from “measured” and “ready to deploy.”

It does not replace a benchmark runner. It makes the decision around a benchmark more trustworthy.

## Why this is better than the usual workflow

The usual optimization workflow is fast but fragile: change a setting, run a benchmark, keep the
best chart, then try to reconstruct what changed when someone asks whether the result transfers.
That approach makes it easy to tune against the holdout set, compare against a moving baseline,
omit failed trials or overhead, and turn one favorable run into a broad claim.

ACE reverses the order:

- **Usual workflow:** result first, methodology reconstructed later.
- **ACE workflow:** baseline, allowed changes, holdout split, trial plan, acceptance rules, and
  evidence-retention plan are declared before measurement.
- **Usual output:** a score or chart that needs explanation.
- **ACE output:** a score can be accompanied by a compact decision record showing what was tested,
  what was held constant, what remains uncertain, and whether the result is ready to act on.

ACE is not better because it produces a higher benchmark score. It is better when the cost of a
false win is high: it makes a weak result easier to reject early and a real win easier to defend.

The core value is not any individual finding. It is the capacity to tell when an optimization claim is true, false, or only conditionally true — with traceable evidence at every verdict.

---

## Research context

Optimization claims in AI systems are routinely reported as global improvements — even when they are valid only in narrow operating conditions. Average-case benchmarks hide regime boundaries. Single-run results get promoted. Overheads get omitted. False wins compound.

The result: teams deploy optimizations that collapse under production load.

---

## Research-system capabilities

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

## Historical simulated study: Token Pruning Has a Hard Failure Boundary

This earlier, simulated-telemetry study remains in the repository as a framework-development
example. It is not ACE's primary public reference application and should not be read as a measured
hardware-energy result. For a current retained-evidence workflow, use Token-Bleed R5 above.

**Thesis:** Token pruning ECD gains are regime-bounded by sequence length and batch size. Outside the validated envelope, ECD degrades deterministically. This is a systems-boundary failure, not noise.

| Region | Sequence Length | Batch Size | ECD Outcome |
|---|---|---|---|
| Strong positive | ≤ 256 | ≤ 4 | Consistent gain |
| Edge of viability | 384 | ≤ 2 | Marginal |
| Boundary | 128–512 | 3–6 | Mixed |
| Collapse | > 512 | > 4 | Deterministic loss |

**Deployment implication:** Token pruning should not be accepted or rejected on average. Rollout should be gated on sequence-length and batch-size ceilings, not aggregate ECD.

**Telemetry caveat:** This result was produced under simulated power telemetry (`ACE_DIRECT_POWER_WATTS` override). It is useful for exercising boundary logic, not for a measured energy-efficiency claim.

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
├── src/ace_lab/                 # Installable stable package
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
pip install .
ace validate experiments/near_term/exp_002_token_pruning.yaml
ace preflight experiments/near_term/exp_002_token_pruning.yaml
ace run experiments/near_term/exp_002_token_pruning.yaml --output ./ace-artifacts
ace assess experiment.yaml retained-trials.json --output ./ace-assessment
```

`ace run` records a validated contract, provenance manifest, and Markdown run record. It does
not generate workload measurements or an optimization claim. The repository's simulation agents,
demo scripts, and experimental kernels remain research tooling rather than the public package API.

`ace assess` is the post-run counterpart: it imports retained JSON or CSV trial evidence and checks
it against the exact contract. It produces an `ACCEPTED`, `REJECTED`, or `INCONCLUSIVE` decision
pack, but never creates measurements, fills missing evidence, or independently verifies collection.
When a contract declares independent claims, ACE carries each retained claim verdict into the
decision pack instead of silently collapsing it into the generic verdict. See the
[worked assessment example](docs/USING_ACE.md#assess-retained-evidence-after-the-run) and
[claim-scoped assessments](docs/CLAIM_SCOPED_ASSESSMENTS.md).

For a copy-paste retained-evidence walkthrough, including the R5 public-packet verification path,
see [`docs/RETAINED_EVIDENCE_WORKFLOW.md`](docs/RETAINED_EVIDENCE_WORKFLOW.md).

The package is a complement to standardized benchmark suites, not a replacement for them. See
[`docs/PACKAGE_POSITIONING.md`](docs/PACKAGE_POSITIONING.md) for its category, boundaries, and
release posture.

See the
[`v0.1.0 release notes`](docs/RELEASE_NOTES_v0.1.0.md) for the supported workflow, JSON/CSV
import boundary, and verdict interpretation.

See [`GETTING_STARTED.md`](GETTING_STARTED.md) for the full seven-element experiment walkthrough.

---

## Documentation

| Document | Purpose |
|---|---|
| [`docs/VALIDATED_RESULTS.md`](docs/VALIDATED_RESULTS.md) | Validated findings with theses, caveats, and deployment implications |
| [`GETTING_STARTED.md`](GETTING_STARTED.md) | Quickstart and 7-element experiment walkthrough |
| [`docs/USING_ACE.md`](docs/USING_ACE.md) | Plain-language guide to what ACE helps people do |
| [`docs/TRIAL_EVIDENCE_FORMAT.md`](docs/TRIAL_EVIDENCE_FORMAT.md) | JSON/CSV evidence contract for `ace assess` |
| [`docs/RETAINED_EVIDENCE_WORKFLOW.md`](docs/RETAINED_EVIDENCE_WORKFLOW.md) | Copy-paste assessment workflow and public R5 verification |
| [`docs/RELEASE_NOTES_v0.1.4.md`](docs/RELEASE_NOTES_v0.1.4.md) | License-file release notes |
| [`docs/RELEASE_NOTES_v0.1.3.md`](docs/RELEASE_NOTES_v0.1.3.md) | Retained-evidence reliability release notes |
| [`docs/CLAIM_SCOPED_ASSESSMENTS.md`](docs/CLAIM_SCOPED_ASSESSMENTS.md) | Independent decision scopes and fail-closed coverage |
| [`docs/REFERENCE_APPLICATION_TOKEN_BLEED_R5.md`](docs/REFERENCE_APPLICATION_TOKEN_BLEED_R5.md) | Public reference application of generic and claim-scoped assessments |
| [`docs/RELEASE_NOTES_v0.1.0.md`](docs/RELEASE_NOTES_v0.1.0.md) | Installed package workflow and verdict boundaries |
| [`docs/PACKAGE_POSITIONING.md`](docs/PACKAGE_POSITIONING.md) | Category, before/after workflow, and claim boundaries |
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
