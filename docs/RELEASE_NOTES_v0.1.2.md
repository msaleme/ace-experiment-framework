# ACE v0.1.2 release notes

ACE v0.1.2 makes claim-scoped assessment a supported package feature.

- Contracts may declare independent `claim_scopes`.
- Evidence may retain one `ACCEPTED`, `REJECTED`, or `INCONCLUSIVE` verdict per scope.
- ACE requires exact declared-to-retained scope coverage and returns `INCONCLUSIVE` when a scope
  is missing or mismatched.
- Decision packs and Markdown reports display generic and claim-scoped decisions separately.

The package still reconciles retained evidence only. It does not execute the workload, independently
reproduce data collection, or turn an accepted narrow claim into a production or deployment claim.
