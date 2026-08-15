# ACE trial-evidence format

`ace assess` consumes retained evidence from an actual runner. It does not run the workload, infer
missing values, or upgrade a provenance label. Use this format to keep the evidence and the
experiment contract reviewable together.

The machine-readable definitions are:

- [`schemas/ace-trial-evidence-v1.json`](../schemas/ace-trial-evidence-v1.json)
- [`schemas/ace-decision-pack-v1.json`](../schemas/ace-decision-pack-v1.json)

## JSON evidence

The input is one JSON object with these required fields:

- `schema_version`: `"1.0"`
- `artifact_type`: `"ace-trial-evidence"`
- `experiment_id` and `config_sha256`: must identify the exact YAML contract passed to `ace assess`
- `source_revision`: revision of the runner or workload source, retained by the user
- `telemetry_provenance`: one of `measured`, `estimated`, or `simulated`
- `baseline_metrics`: numeric baseline value for the configured quality metric
- `trials`: trial records with a unique `trial_id`, integer `seed`, ACE split, `success`, `metrics`, and `metric_sources`

A failed trial must include `success: false` and a non-empty `error_message`. Failed trials are
retained and counted; they are never dropped from the assessment record.

When the contract requires significance or a confidence interval that excludes zero, include
`statistical_evidence.development.p_value` and
`statistical_evidence.development.ecd_confidence_interval` respectively. ACE marks the result
`INCONCLUSIVE` rather than guessing those values.

The complete synthetic example is
[`examples/assess-evidence/retained-trials.json`](../examples/assess-evidence/retained-trials.json).

## CSV evidence

CSV is supported for runners that export tabular records. Each row repeats these metadata columns:

`experiment_id`, `config_sha256`, `source_revision`, `telemetry_provenance`, `trial_id`, `seed`,
`split`, `success`, `metrics_json`, and `metric_sources_json`.

`metrics_json` and `metric_sources_json` are JSON objects stored in a CSV cell. Optional
`baseline_metrics_json`, `statistical_evidence_json`, and `error_message` columns carry the same
data as the JSON form. Metadata values must be identical and non-empty across every CSV row.

## Decision meaning

`ACCEPTED` means supplied evidence reconciles with the contract and passes its stated checks.
`REJECTED` means complete supplied evidence fails a stated check. `INCONCLUSIVE` means identity,
coverage, provenance, baseline, metric, or required statistical evidence is missing or mismatched.

None of those verdicts independently verifies collection, reproduces a result, certifies a system,
or proves production transfer.
