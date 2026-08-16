# ACE v0.1.0 release notes

ACE v0.1.0 is the first installable release of the experiment-contract and retained-evidence
assessment workflow.

## Core promise

Preflight the experiment. Retain the evidence. Assess whether a claimed win is trustworthy.

ACE helps teams decide what must be true before a result can support a decision. It does not run a
benchmark workload, create measurements, attest to data collection, or certify a deployment.

## Included workflow

- `ace validate` checks a declared experiment contract.
- `ace preflight` identifies coverage, provenance, and evidence gaps before measurement begins.
- `ace run` retains the contract, runtime provenance, and claim boundary without fabricating a
  workload result.
- `ace assess` imports retained trial evidence in generic JSON or CSV form and produces an
  `ACCEPTED`, `REJECTED`, or `INCONCLUSIVE` decision pack against the exact declared contract.

The JSON/CSV formats and a complete synthetic example are documented in
[`TRIAL_EVIDENCE_FORMAT.md`](TRIAL_EVIDENCE_FORMAT.md).

## How to interpret the verdict

`ACCEPTED` is not a deployment certification or independent reproduction. It means the supplied
evidence reconciles with the contract and passes the contract's explicit rules.

`REJECTED` is a completed result, not a broken workflow: the retained evidence is complete but a
declared rule failed. Preserve it and do not turn it into a positive comparative claim.

`INCONCLUSIVE` is the fail-closed result for missing, mismatched, or insufficient evidence. It is
an instruction to retain the gap and resolve it, not to fill it with an assumption.

## Installed-wheel support

The release includes ACE's immutable built-in benchmark profiles in the installed wheel. Profile
resolution uses package resources and rejects invalid profile identities, so a fresh wheel install
does not depend on files from a source checkout.

## Boundaries

ACE reconciles user-supplied evidence. It does not independently reproduce a run, verify that a
provider executed it, or establish general performance beyond the exact contract and environment.
