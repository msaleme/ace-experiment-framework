# Synthetic assessment example

This directory is a format walkthrough only. Its numbers are invented and must not be cited as an
ACE benchmark result or a performance claim.

Run it from the repository root:

```bash
ace assess examples/assess-evidence/experiment.yaml \
  examples/assess-evidence/retained-trials.json --output ./ace-assessment-example
```

The evidence file carries the SHA-256 digest of the included YAML contract. Change the contract and
the assessment becomes `INCONCLUSIVE` until evidence is regenerated with the new digest.
