# ACE package positioning

## The category

ACE is experiment-contract tooling for AI and systems optimization research.

It sits before a benchmark result is promoted: it validates the declared baseline, mutation scope,
development/validation/holdout split, trial plan, acceptance rules, and reporting contract, then
records a provenance-bearing run artifact. Its first package command deliberately does **not**
generate performance numbers. A validated contract is not a measured outcome.

## What ACE is not

- Not an MLPerf implementation, submission tool, or replacement for a standardized benchmark.
- Not a hardware leaderboard or a promise that an optimization transfers across systems.
- Not a general experiment tracker, model-training framework, or automatic optimizer.
- Not evidence that a simulated or recorded result is independently reproduced.

## Why this position is defensible

MLPerf supplies standardized workload, accuracy, latency, and submission requirements for comparable
system benchmarking. ACE complements that discipline when a team is testing its own optimization and
needs to prevent scope drift, baseline drift, hidden holdout reuse, or a single favorable run becoming
a general claim. ACE's useful output is a bounded claim package, not a score.

## Intended users and first use case

Research engineers and evaluation owners who run a non-standard optimization experiment and need an
auditable pre-results contract. Start by running `ace validate` against a checked-in experiment YAML,
then `ace run` to retain the immutable config digest, package/runtime versions, declared seeds,
telemetry provenance, and claim boundary alongside the work record.

## Practical benefit

ACE reduces the cost of being wrong about a “win.” Before compute is spent, it makes the researcher
declare what changes, what remains fixed, which data are held out, how many trials are expected, and
what result would count. Before a decision is made, it gives the reviewer a compact record of the
plan, missing evidence, provenance, and claim limit. That is useful whether the finding is accepted,
rejected, or inconclusive.

## The before-and-after workflow

**Before ACE:** a team tunes an optimization, shares its strongest run, and asks reviewers to infer
the baseline, scope, trial selection, holdout use, and measurement provenance from notebooks,
messages, and memory. Review happens after the conclusion has momentum.

**With ACE:** the team writes the experiment contract first, runs `ace preflight` to expose gaps,
and retains the resulting plan and claim boundary with the work. Reviewers can ask a much better
question: not “does this chart look good?” but “does this result meet the conditions we agreed would
make it decision-worthy?”

That is the advantage. ACE does not promise better hardware performance. It reduces the chance that
a team mistakes an attractive benchmark result for a deployable finding.

## Positioning line

**ACE makes an optimization claim earn its evidence before it earns a chart.**

## Release posture

The package should first be released as a beta contract-and-provenance tool. Do not market it as
measured-performance software until an adapter produces retained measurements under a declared
environment. Do not represent its artifacts as independent validation or standardized benchmark
submissions.
