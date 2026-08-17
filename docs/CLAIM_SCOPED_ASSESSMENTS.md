# Claim-scoped assessments

An experiment can support one claim and reject another. ACE permits a contract to declare
independent `claim_scopes` and retained evidence to supply a verdict for each scope.

```yaml
claim_scopes:
  cost_vs_full: {comparison: governed-vs-full}
  value_vs_lexical: {comparison: governed-vs-lexical}
```

The retained JSON evidence must include exactly the same names under
`claim_scoped_verdicts`. Every scope retains an `ACCEPTED`, `REJECTED`, or `INCONCLUSIVE`
verdict. A partial or mismatched set fails closed.

The generic ACE verdict and claim-scoped verdicts are intentionally separate. The generic verdict
assesses shared contract gates. Claim scopes preserve the domain-specific evidence adapter's
decisions. An accepted cost claim does not imply an accepted quality, baseline-superiority,
production, or deployment claim.
