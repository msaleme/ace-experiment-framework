# Verification Pack

Generated: 2026-03-27T13:41:36.348594Z

## Summary
- Total experiments: 29
- Accepted: 23
- Rejected: 6

## Implementation Inventory
- Phase 1 - Adaptive INT8/INT4 quantization: M5, substantive=True, metrics=mocked/synthetic benchmarked
- Phase 1 - Dynamic sparsity / token pruning: M5, substantive=True, metrics=mocked/synthetic benchmarked
- Phase 1 - Memory-traffic reduction: M5, substantive=True, metrics=mocked/synthetic benchmarked
- Phase 1 - Compiler graph optimization: M5, substantive=True, metrics=mocked/synthetic benchmarked
- Phase 2 - RNS emulator: M2/M3, substantive=True, metrics=estimated/simulated
- Phase 2 - LNS comparison harness: M2/M3, substantive=True, metrics=estimated/simulated
- Phase 2 - Heterogeneous arithmetic boundary testing: M2/M3, substantive=True, metrics=estimated/simulated
- Phase 2 - Event-driven workload harness: M2/M3, substantive=True, metrics=estimated/simulated
- Phase 3 - Analog / photonic / in-memory adapters: M2/M3, substantive=True, metrics=estimated/simulated

## Top 5 Credible Wins
1. exp_003_int4_static_quant_sweep (near_term): ECD delta=0.5603, quality delta=-0.0170, latency delta=-17.97ms, energy delta=-0.1126J
2. exp_002_token_pruning (near_term): ECD delta=0.3802, quality delta=-0.0469, latency delta=-14.62ms, energy delta=-0.0916J
3. exp_006_token_pruning_threshold_sweep (near_term): ECD delta=0.3802, quality delta=-0.0469, latency delta=-14.62ms, energy delta=-0.0916J
4. exp_004_compiler_fusion (near_term): ECD delta=0.2275, quality delta=0.0000, latency delta=-8.45ms, energy delta=-0.0528J
5. exp_008_kernel_fusion_loop (near_term): ECD delta=0.2275, quality delta=0.0000, latency delta=-8.45ms, energy delta=-0.0528J

## Integrity Highlights
- Critical: holdout declared but no independent holdout scoring in execution loop.
- High: synthetic/mock metrics dominate; not real hardware benchmarks.
- High: many collected metrics are not decision-gating in verdict logic.

## Full Data
- See verification_pack.json for complete acceptance audit table and decision traces.