# Using ACE

ACE is for the point just before a team believes an optimization result.

It does not run a GPU benchmark for you. It helps make sure the benchmark you run can support a
decision later.

## The problem it solves

A common workflow is: tune an optimization, find a good chart, then explain the method after the
fact. That makes it hard to tell whether the comparison used a fixed baseline, whether a holdout was
protected, whether failed trials were retained, or whether a power number was measured or estimated.

ACE makes those questions visible before measurement. The goal is simple: do not let a promising
result become a deployment decision until the evidence needed to support it has been declared and
retained.

## Who should use it

- An engineer comparing a quantization, pruning, compiler, or memory optimization.
- A research lead reviewing whether an apparent gain is ready for a decision.
- A platform or evaluation team that needs a lightweight record of what was fixed, changed, and
  still uncertain.

## Four commands, four jobs

```bash
pip install ace-experiment-framework

# 1. Is the plan structurally complete?
ace validate experiment.yaml

# 2. What must happen before this result is trustworthy enough to measure?
ace preflight experiment.yaml

# 3. Preserve the validated plan and its claim boundary with the work.
ace run experiment.yaml --output ./ace-artifacts

# 4. Reconcile retained trial evidence with the exact plan after the run.
ace assess experiment.yaml retained-trials.json --output ./ace-assessment
```

`ace validate` checks the required experiment-contract fields.

`ace preflight` produces a practical checklist: development, validation, and holdout coverage;
seed/trial consistency; telemetry-provenance gaps; and the next evidence-retention steps.

`ace run` writes a provenance manifest and Markdown record. Its initial verdict is
`INCONCLUSIVE` on purpose. A plan is not a measurement, and a measurement is not automatically a
deployment recommendation.

## Assess retained evidence after the run

`ace assess` is the bridge between a plan and a review. Give it the original experiment YAML and
the evidence you retained from the actual runner. ACE checks that the experiment ID and config
digest match; that all three splits, declared seeds, and trial coverage are present; that failed
trials were retained; and that telemetry, baseline, quality, ECD, complexity, and required
statistical evidence can support the declared rules.

It writes a JSON decision pack and a short Markdown assessment. Its verdict is intentionally
bounded:

- `ACCEPTED` means the supplied evidence reconciles with the contract and passes its explicit rules.
- `REJECTED` means the evidence is complete but one or more rules fail.
- `INCONCLUSIVE` means the evidence is missing, mismatched, or cannot support the required rule.

It does not run a benchmark, silently substitute a value, attest to how evidence was collected, or
independently reproduce a result. The sample in
[`examples/assess-evidence/`](../examples/assess-evidence/) is deliberately synthetic and is a
format walkthrough, not a benchmark finding.

## Reading the preflight

`ready_to_measure: true` means the declared contract has explicit seeds, telemetry provenance, and
the required split structure. It does **not** mean the optimization works.

`ready_to_measure: false` means ACE has found a declared-evidence gap. Fix the gap, or retain it as
a limitation. For example, if power data are not labelled measured, estimated, or simulated, ACE
will not let that omission disappear behind an energy-efficiency chart.

## What happens after ACE

Run the actual workload with the declared environment and trial plan. Retain raw metrics, failed
trials, telemetry source, source revision, and the decision trace. Then use `ace assess` to
evaluate the retained result against the acceptance rules and state the operating envelope. ACE
makes this process reviewable; it does not substitute for the benchmark runner, a domain expert,
or independent reproduction.

## What ACE does not claim

- It does not produce a performance score or make hardware faster.
- It does not certify a system or replace MLPerf or another standardized benchmark.
- It does not prove that a result transfers to another model, workload, device, or production system.
- It does not turn simulation data into a measured result or a result into independent validation.
