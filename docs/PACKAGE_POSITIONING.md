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

## Positioning line

**ACE makes an optimization claim earn its evidence before it earns a chart.**

## Release posture

The package should first be released as a beta contract-and-provenance tool. Do not market it as
measured-performance software until an adapter produces retained measurements under a declared
environment. Do not represent its artifacts as independent validation or standardized benchmark
submissions.
