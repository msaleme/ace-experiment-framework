# ACE v0.1.3 - retained-evidence reliability

## Purpose

This release does not add a new benchmark finding or change any Token-Bleed verdict. It makes the
released retained-evidence workflow easier to use and harder to misstate.

## Changes

- Makes Token-Bleed R5 the primary public reference application.
- Adds a copy-paste workflow for assessing retained evidence and verifying the public R5 packet.
- Adds regression coverage that preserves the independent R3/R5 claim structure: accepted
  governed-versus-full claims do not overwrite rejected governed-versus-lexical claims.
- Reclassifies the earlier token-pruning analysis as a historical simulated-telemetry framework
  study, not a measured hardware-energy result.

## Compatibility and claim boundary

The retained-evidence JSON schema remains `1.0`. This release can assess the public R3 and R5
evidence packets without changing their generic or claim-scoped verdicts. It does not validate the
private raw reports, certify collection, or make cross-model or production claims.
