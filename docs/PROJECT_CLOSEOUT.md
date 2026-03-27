# Project Closeout

## Summary

ACE Experiment Framework is a config-driven research system for evaluating compute-efficiency ideas under explicit anti-self-deception controls. The project now includes the core orchestration layer, baseline and benchmark integrity controls, split-aware verdicting, telemetry provenance, benchmark-specific quality scoring, and focused decision packages for token pruning boundary analysis.

This closeout documents what was built, what was validated, what remains constrained by environment, and which artifacts represent the final state of the project at closeout.

## Final Scope

- Phase 1 foundation modules completed.
- Phase 2 experimentation workflow implemented.
- Hardening pass completed for:
  - independent development / validation / holdout execution
  - single decision engine with explicit gate traces
  - telemetry provenance and uncertainty accounting
  - skeptic review with instability diagnostics
- Token-pruning analysis completed as a bounded-regime study for:
  - `exp_002_token_pruning`
  - `exp_006_token_pruning_threshold_sweep`

## Delivered Architecture

Core framework:

- `src/model.py`: shared records, enums, and serialization structures
- `src/baseline_manager.py`: immutable baseline snapshots and integrity checks
- `src/benchmark_registry.py`: development / validation / holdout benchmark separation
- `src/metrics_collector.py`: trial persistence, split summaries, provenance-aware aggregation
- `src/experiment_runner.py`: config-driven execution and split-aware orchestration
- `src/stats_evaluator.py`: effect size, significance, CI, and outlier handling
- `src/decision_engine.py`: single verdict source with explicit gate coverage
- `src/report_generator.py`: report generation and artifact packaging

Telemetry and evaluation:

- `src/near_term_telemetry.py`: measured runtime path, power/energy source hierarchy, uncertainty propagation
- `src/benchmark_quality.py`: benchmark-specific quality scoring for token pruning and compiler fusion
- `agents/skeptic/skeptic_agent.py`: skepticism layer with normalized instability rule
- `agents/build/build_agent.py`: experiment family wiring to executors and telemetry wrapper

## Validation State

- Unit and hardening tests were added and run during implementation.
- Latest validated state for the sprinted hardening path was `11 passed`.
- Token-pruning regime and holdout analyses were run as focused reports rather than as acceptance-seeking experiments.

## Final Findings

### Token Pruning

Token pruning is not a universal optimization in the current implementation. It is useful only in a bounded operating envelope.

Consensus operating envelope:

- strong positive region: sequence length up to 256 with batch up to 4
- edge region: `384 x <=2`, `512 x 1`
- boundary region: `128 x 6`, `384 x 3`, `512 x 2`
- collapse region: larger sequence lengths and larger batches beyond that envelope

Interpretation:

- dominant practical boundaries are sequence length and batch size
- hidden size and depth are not primary boundary variables in the current implementation
- failure beyond the envelope is primarily a systems-boundary problem, not a random-quality-collapse problem

## Key Artifacts

Closeout and onboarding:

- `README.md`
- `GETTING_STARTED.md`
- `MANIFEST.md`
- `docs/PROJECT_CLOSEOUT.md`

Hardening and telemetry:

- `docs/telemetry_variance_protocol.md`
- `reports/holdout_transfer_diagnosis_token_pruning.md`
- `reports/token_pruning_boundary_conditions.md`

Decision artifacts:

- `reports/token_pruning_decision_memo.md`
- `reports/token_pruning_2d_regime_table.md`
- `reports/token_pruning_direct_power_decision_package.md`

## Environment Constraints At Closeout

- Native `nvidia-smi` direct telemetry was not available on the host used for the latest focused runs.
- Direct power-path analysis therefore used the `ACE_DIRECT_POWER_WATTS` override path for direct-source simulation.
- This affects provenance strength, but it does not remove the observed runtime-envelope boundary pattern in the token-pruning study.

## Known Limitations

- `exp_002_token_pruning` and `exp_006_token_pruning_threshold_sweep` currently route through the same default pruning executor path, so the final boundary characterization is effectively family-level.
- Hidden size is not materially wired into the measured workload path used by the synthetic boundary sweep.
- Layer depth has limited leverage in the current pruning kernel because the effective pruning ratio stays nearly constant across tested depths.

## Recommended Next Work

If the project is extended beyond closeout, the highest-value next steps are:

1. Run the token-pruning boundary map on hardware with native direct device telemetry.
2. Wire hidden-size and depth more faithfully into the measured workload path.
3. Separate token-pruning family members into materially distinct executor configurations before claiming experiment-level independence.
4. Add deployment guardrails that enforce the positive operating envelope directly.

## Closeout Status

Project status at closeout: completed and documented for public publication as a research framework with bounded-regime token-pruning findings.