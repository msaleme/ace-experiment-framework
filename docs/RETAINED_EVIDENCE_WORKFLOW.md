# Retained evidence workflow

ACE evaluates evidence that an experiment runner has already retained. It does not run the
workload, recreate missing rows, or independently attest to collection.

## Assess your own completed run

Keep the original contract and a JSON or CSV evidence file together, then run:

```bash
python -m pip install ace-experiment-framework==0.1.3
ace validate experiment.yaml
ace preflight experiment.yaml
ace assess experiment.yaml retained-trials.json --output ./ace-assessment
sha256sum ./ace-assessment/*.decision-pack.json
```

The decision pack reports a generic contract verdict, individual claim verdicts when the contract
declares `claim_scopes`, failed generic gates, retained evidence gaps, and the contract digest.
Treat the decision-pack SHA-256 as an identifier for that exact rendered artifact, not as proof of
independent collection.

## Verify the public Token-Bleed R5 reference packet

R5 is the public reference application for claim-scoped assessment. Its raw Mac report remains
private because it contains host identifiers. The public packet contains a frozen contract,
preflight, derived ACE evidence, decision pack, and a manifest committing to the raw-report hash.

```bash
git clone https://github.com/msaleme/token-bleed-benchmark.git
cd token-bleed-benchmark
python -m pip install ace-experiment-framework==0.1.3
python scripts/verify_r5_public_evidence.py --ace-command ace
```

Expected R5 boundary:

- Generic assessment, governed-versus-full cost, and governed-versus-full quality are `ACCEPTED`.
- Governed-versus-lexical value and routing-miss sensitivity are `REJECTED` under the frozen 3x
  lexical prompt-cost ceiling.

The verification script checks the public hashes and 540-row preflight matrix, then regenerates an
ACE decision pack from the published ACE evidence. It does not make R5 cross-model, production,
or governance-always-wins evidence.

## Compatibility commitment

ACE keeps the R3 and R5 public claim structures as compatibility references. A change that alters
their generic or claim-scoped verdicts requires a new package version, an explicit explanation,
and a new assessment artifact. It must never silently rewrite a released verdict.
