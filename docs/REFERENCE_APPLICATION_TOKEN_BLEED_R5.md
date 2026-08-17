# Reference Application: Token-Bleed R5

## Purpose

Token-Bleed R5 is a public reference application of ACE's retained-evidence assessment workflow.
It demonstrates how a completed empirical result can contain a valid narrow finding and a rejected
economic comparison at the same time.

- **Benchmark runner:** Token-Bleed generated the synthetic catalogs, called the declared local
  endpoint, retained the reports, and scored answer quality.
- **ACE:** validated the frozen experiment contract, reconciled retained trial evidence, and
  rendered generic and claim-scoped decision records.

ACE did not execute the benchmark, independently attest to the Mac collection, or certify a
production deployment.

## Public evidence

- [R5 immutable release](https://github.com/msaleme/token-bleed-benchmark/releases/tag/r5-results-2026-08-17)
- [R5 result and claim boundary](https://github.com/msaleme/token-bleed-benchmark/blob/main/docs/R5_RESULTS.md)
- [Frozen contract](https://github.com/msaleme/token-bleed-benchmark/blob/main/experiments/token-bleed-mac-r5.yaml)
- [Public ACE evidence](https://github.com/msaleme/token-bleed-benchmark/blob/main/evidence/token-bleed-mac-r5/ace-evidence.json)
- [Public ACE decision pack](https://github.com/msaleme/token-bleed-benchmark/blob/main/evidence/token-bleed-mac-r5/ace-decision-pack.json)

The original raw report is intentionally private because its hardware provenance contains host
identifiers. Its original SHA-256 is retained in the public manifest.

## R5 decision structure

| Claim | Comparator | Verdict |
|---|---|---:|
| Generic contract assessment | Governed versus raw full context | **ACCEPTED** |
| Selective-context cost | Governed versus raw full context | **ACCEPTED** |
| Governed quality | Governed versus raw full context | **ACCEPTED** |
| Governed value | Governed versus lexical filter | **REJECTED** |
| Routing-miss sensitivity | Governed versus lexical filter at 5% and 10% misses | **REJECTED** |

The rejected claims do not negate the accepted full-context comparison. They prevent a different,
unsupported conclusion: that governed context is automatically cost-effective against every cheap
selective alternative.

## Why claim scopes matter

A single aggregate verdict would have forced an inaccurate choice between two bad summaries:

1. "The experiment failed," which would hide the accepted governed-versus-full result.
2. "Governance wins," which would hide the failed lexical-cost condition.

Claim-scoped assessment preserves the condition that each conclusion actually earned. This is the
kind of anti-self-deception control ACE is designed to provide.

## Rechecking the public packet

The Token-Bleed repository provides a public verification command that checks the published
artifacts and regenerates the ACE decision pack from the public trial evidence. That verification
does not replace the private raw report or turn the release into a production-ROI claim.
