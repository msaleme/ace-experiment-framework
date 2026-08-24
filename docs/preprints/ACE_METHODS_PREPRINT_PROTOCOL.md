# ACE Methods Preprint Protocol

## Claim-scoped assessment for evidence-bound experimental results

**Status:** Not DOI-ready. This protocol defines the evidence required before an ACE methods preprint can be deposited.

## 1. Proposed contribution

ACE is a claim-scoped assessment workflow for experimental result packets. Rather than promoting one aggregate verdict, it keeps declared comparators, acceptance rules, evidence coverage, and limitations attached to each claim. The proposed paper will evaluate whether this approach preserves supported and unsupported claims, and fails closed when required evidence is absent or inconsistent.

The paper must not claim that ACE certifies systems, verifies private raw data, or establishes cross-domain generality from one reference application.

## 2. Research question

Can a contract-bound assessor preserve distinct supported and unsupported claims from supplied evidence, while failing closed for missing, incomplete, or mismatched evidence?

## 3. Current evidence

The current reference application is Token-Bleed R5. It provides:

- a frozen experiment contract;
- a privacy-safe public evidence packet;
- independently assessed governed-versus-full and governed-versus-lexical claim scopes;
- prior R4 fail-closed boundaries where full-context comparability was incomplete; and
- regression tests intended to preserve separate R3 and R5 claim scopes.

This is useful reference evidence, but it is not sufficient on its own for a general ACE methods preprint.

## 4. Minimum evidence required before DOI deposit

A DOI preprint requires all of the following:

1. A second, structurally distinct application beyond Token-Bleed.
2. An adversarial mutation evaluation covering, at minimum:
   - missing required rows;
   - altered artifact digests;
   - changed comparator baselines;
   - incomplete claim scopes; and
   - mismatched contract and evidence fields.
3. A frozen public protocol and a public result packet for each application.
4. A comparison with a non-claim-scoped baseline at the tested properties.
5. A limitations section that states ACE evaluates supplied evidence rather than independently verifying private raw data or certifying production safety.
6. A complete reproducibility bundle: versioned source, tests, citation metadata, hashes, license, and rendered paper PDF.

## 5. Evaluation design

For each application, authors must declare claims before assessment. Each claim must name its comparator, evidence requirements, and pass or fail rule. The evaluation should report:

- whether each claim is accepted, rejected, or inconclusive;
- whether mutations were detected and caused the expected fail-closed result;
- whether a non-claim-scoped summary would have obscured an unsupported or incomplete claim; and
- the boundaries that remain outside ACE's evidence scope.

The second application must differ materially in data structure, comparator logic, or failure modes from Token-Bleed. It may not simply be a rerun of the same workload.

## 6. Paper structure after evidence is complete

1. Abstract and bounded contribution
2. Background: aggregate verdicts versus claim scopes
3. ACE contract and assessment model
4. Applications and frozen protocols
5. Mutation evaluation and fail-closed results
6. Comparison baseline
7. Limitations and threats to validity
8. Reproducibility and artifact availability

## 7. Deposit gate

Do not mint a DOI until the requirements in section 4 are evidenced in the repository and the manuscript has passed a claim-language review. The Token-Bleed R5 result can be cited as a reference application, but it must not be represented as sufficient validation of ACE as a general method.

