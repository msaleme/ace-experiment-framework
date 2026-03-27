# Full Framework Verification Pack

Generated: 2026-03-27T13:41:36.348594Z

## 1) Implementation Inventory

| Family | File Paths | Maturity | Logic | Metrics |
|---|---|---|---|---|
| Phase 1 - Adaptive INT8/INT4 quantization | src/kernels/quantization.py; experiments/near_term/exp_001_int4_quantization.yaml; experiments/near_term/exp_002_int8_static_quant_sweep.yaml; experiments/near_term/exp_003_int4_static_quant_sweep.yaml; experiments/near_term/exp_004_per_layer_mixed_precision_search.yaml | M5 | Substantive (Substantive kernel logic with per-layer/fallback behavior and trial execution.) | mocked/synthetic benchmarked |
| Phase 1 - Dynamic sparsity / token pruning | src/kernels/sparsity.py; experiments/near_term/exp_002_token_pruning.yaml; experiments/near_term/exp_006_token_pruning_threshold_sweep.yaml; experiments/near_term/exp_007_sparse_activation_routing.yaml | M5 | Substantive (Substantive pruning math and trial generation; synthetic metrics.) | mocked/synthetic benchmarked |
| Phase 1 - Memory-traffic reduction | src/kernels/memory_optimization.py; experiments/near_term/exp_003_memory_optimization.yaml; experiments/near_term/exp_009_memory_layout_cache_policy.yaml; experiments/near_term/exp_010_retrieval_vs_recompute.yaml | M5 | Substantive (Substantive recomputation/storage tradeoff logic; synthetic metrics.) | mocked/synthetic benchmarked |
| Phase 1 - Compiler graph optimization | src/kernels/compiler_optimization.py; experiments/near_term/exp_004_compiler_fusion.yaml; experiments/near_term/exp_008_kernel_fusion_loop.yaml | M5 | Substantive (Substantive fusion/tiling simulation logic; synthetic metrics.) | mocked/synthetic benchmarked |
| Phase 2 - RNS emulator | simulators/mid_term_simulator.py; experiments/mid_term/exp_011_rns_emulator.yaml; experiments/mid_term/exp_012_rns_modulus_search.yaml | M2/M3 | Substantive (Executable proxy simulator with estimated conversion overhead.) | estimated/simulated |
| Phase 2 - LNS comparison harness | simulators/mid_term_simulator.py; experiments/mid_term/exp_013_lns_kernel_comparison.yaml; experiments/mid_term/exp_014_posit_simulation.yaml; experiments/mid_term/exp_015_ternary_representation.yaml | M2/M3 | Substantive (Executable representation proxy harness; simulation-only metrics.) | estimated/simulated |
| Phase 2 - Heterogeneous arithmetic boundary testing | simulators/mid_term_simulator.py; experiments/mid_term/exp_016_heterogeneous_boundary_search.yaml | M2/M3 | Substantive (Boundary-placement modeled in proxy simulator.) | estimated/simulated |
| Phase 2 - Event-driven workload harness | simulators/mid_term_simulator.py; experiments/mid_term/exp_017_async_execution_emulator.yaml; experiments/mid_term/exp_018_fpga_resource_mapping.yaml | M2/M3 | Substantive (Event-driven behavior approximated in executable simulator.) | estimated/simulated |
| Phase 3 - Analog / photonic / in-memory adapters | simulators/moonshot_simulator.py; experiments/moonshot/exp_019_analog_mac_noise_sweep.yaml; experiments/moonshot/exp_020_analog_calibration_overhead.yaml; experiments/moonshot/exp_021_photonic_linear_algebra_model.yaml; experiments/moonshot/exp_022_optical_boundary_cost.yaml; experiments/moonshot/exp_023_in_memory_compute_model.yaml; experiments/moonshot/exp_024_endurance_drift_sensitivity.yaml; experiments/moonshot/exp_025_neuromorphic_temporal.yaml | M2/M3 | Substantive (Executable moonshot adapters with synthetic/estimated metrics.) | estimated/simulated |

## 2) Acceptance Audit (23 accepted, 6 rejected)

| Experiment ID | Hypothesis | Horizon | Baseline | Benchmark | Trials | ECD ? | Quality ? | Latency ? (ms) | Energy ? (J) | Holdout Result | Decision Trace | Reason | Verdict |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| exp_001_bf16_baseline_freeze | BF16 baseline freeze establishes immutable reference with reproducible measurement envelope. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.000000 | -0.000515 | -0.621525 | -0.004508 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=0.0; sig=False; p=nan; ci=[0.0, 0.0]; ci_ex0=False; quality_ok=False | effect_below_threshold,not_significant,ci_includes_zero,quality_floor_failed | rejected |
| exp_001_int4_quantization | Adaptive per-layer INT4 quantization with BF16 fallback improves ECD by at least 15% on transformer inference without violating the 99% quality floor. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.560294 | -0.016979 | -17.965729 | -0.112581 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=9.310099409594297; sig=True; p=6.373742469345318e-09; ci=[0.5124157482604035, 0.6068067138808251]; ci_ex0=True; quality_ok=False | quality_floor_failed | rejected |
| exp_002_int8_static_quant_sweep | INT8 static quantization sweep improves ECD while keeping quality within 1% of baseline. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.560294 | -0.016979 | -17.965729 | -0.112581 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=9.310099409594297; sig=True; p=6.373742469345318e-09; ci=[0.5095314280369498, 0.6092071581926863]; ci_ex0=True; quality_ok=False | quality_floor_failed | rejected |
| exp_002_token_pruning | Dynamic token pruning improves energy efficiency >=20% with bounded quality loss. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.380232 | -0.046929 | -14.617163 | -0.091552 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=4.4149560953458336; sig=True; p=3.982369420329183e-06; ci=[0.30860864336259913, 0.45677038902373746]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_003_int4_static_quant_sweep | INT4 static quantization sweep can improve ECD with acceptable quality floor enforcement. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.560294 | -0.016979 | -17.965729 | -0.112581 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=9.310099409594297; sig=True; p=6.373742469345318e-09; ci=[0.5111893821265174, 0.6094356408234315]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_003_memory_optimization | Selective recomputation reduces memory traffic while preserving output quality. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | -0.215689 | 0.000000 | 11.410886 | 0.071904 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=-5.646697793197405; sig=True; p=4.985962897986838e-07; ci=[-0.24484855684171303, -0.18612810590106937]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_004_compiler_fusion | Kernel fusion reduces p95 latency by >=10% with semantic equivalence. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.227484 | 0.000000 | -8.451146 | -0.052829 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=5.10436044822142; sig=True; p=1.1783921921470223e-06; ci=[0.1895792809695553, 0.26167035145671635]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_004_per_layer_mixed_precision_search | Per-layer mixed precision search improves ECD over uniform precision policies. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.560294 | -0.016979 | -17.965729 | -0.112581 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=9.310099409594297; sig=True; p=6.373742469345318e-09; ci=[0.5102536193070959, 0.6096916184662983]; ci_ex0=True; quality_ok=False | quality_floor_failed | rejected |
| exp_005_activation_quant_sweep | Activation quantization sweep improves ECD while meeting quality floor. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.560294 | -0.016979 | -17.965729 | -0.112581 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=9.310099409594297; sig=True; p=6.373742469345318e-09; ci=[0.5096099026168921, 0.6105160204894422]; ci_ex0=True; quality_ok=False | quality_floor_failed | rejected |
| exp_006_token_pruning_threshold_sweep | Token pruning threshold sweep reduces energy per task by at least 20% with bounded quality loss. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.380232 | -0.046929 | -14.617163 | -0.091552 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=4.4149560953458336; sig=True; p=3.982369420329183e-06; ci=[0.3124419900013257, 0.44889042914679494]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_007_sparse_activation_routing | Sparse activation routing improves ECD via conditional compute paths. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.380232 | -0.046929 | -14.617163 | -0.091552 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=4.4149560953458336; sig=True; p=3.982369420329183e-06; ci=[0.3100491391150863, 0.453932688989921]; ci_ex0=True; quality_ok=False | quality_floor_failed | rejected |
| exp_008_kernel_fusion_loop | Iterative kernel fusion loop reduces p95 latency by at least 10%. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.227484 | 0.000000 | -8.451146 | -0.052829 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=5.10436044822142; sig=True; p=1.1783921921470223e-06; ci=[0.19372121402467504, 0.2632513599168754]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_009_memory_layout_cache_policy | Memory layout and cache policy sweep reduces bytes moved per task. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | -0.215689 | 0.000000 | 11.410886 | 0.071904 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=-5.646697793197405; sig=True; p=4.985962897986838e-07; ci=[-0.24714061698118472, -0.18352487078104804]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_010_retrieval_vs_recompute | Retrieval versus recompute policy improves energy without quality loss. | near_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | -0.215689 | 0.000000 | 11.410886 | 0.071904 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=-5.646697793197405; sig=True; p=4.985962897986838e-07; ci=[-0.24704962734789607, -0.18525784804837023]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_011_rns_emulator | RNS arithmetic kernel emulator yields net ECD gains after conversion overhead. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.151861 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=10.141139913141233; sig=True; p=2.9915356858725377e-09; ci=[0.13736819584960397, 0.16324738770473107]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_012_rns_modulus_search | RNS modulus set search improves arithmetic efficiency and stability. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.150646 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=9.821179950453507; sig=True; p=3.973553648425403e-09; ci=[0.13731130490397636, 0.16390885051953816]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_013_lns_kernel_comparison | LNS multiply-heavy kernels improve energy proxy relative to binary baseline. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.155801 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=12.326661043323284; sig=True; p=5.284110655583522e-10; ci=[0.14576321766609107, 0.1665434617773816]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_014_posit_simulation | Posit representation improves quality-energy tradeoff on selected workloads. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.148804 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=11.852070427869682; sig=True; p=7.494356250754116e-10; ci=[0.13812785203427533, 0.15942233068752462]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_015_ternary_representation | Ternary representation reduces active compute with acceptable quality loss. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.380232 | -0.046929 | -14.617163 | -0.091552 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=4.4149560953458336; sig=True; p=3.982369420329183e-06; ci=[0.3073658265470254, 0.45006215295541335]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_016_heterogeneous_boundary_search | Boundary placement search in heterogeneous arithmetic pipelines improves net ECD. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.145133 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=11.321657706977298; sig=True; p=1.1259978541232714e-09; ci=[0.13457354545109546, 0.15592927649261795]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_017_async_execution_emulator | Asynchronous execution emulation lowers joules per event on sparse temporal workloads. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.145350 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=11.807904969670474; sig=True; p=7.747439875034343e-10; ci=[0.13544534505100114, 0.15509575216580881]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_018_fpga_resource_mapping | FPGA proxy mapping demonstrates viable performance-resource tradeoffs for alternative arithmetic. | mid_term | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 0.161917 | -0.010776 | -5.613679 | -0.049301 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=12.65595760254868; sig=True; p=4.1782528063200534e-10; ci=[0.15196788684132828, 0.17336662553346727]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_019_analog_mac_noise_sweep | Analog MAC noise sweep indicates plausible system-level ECD advantage under bounded drift. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.145981 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=26.566796764443932; sig=True; p=5.469249232861511e-13; ci=[2.0814950837632935, 2.209472734209469]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_020_analog_calibration_overhead | Analog calibration overhead remains below projected efficiency gains. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.113249 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=26.089671375478115; sig=True; p=6.435705488028257e-13; ci=[2.040849200390135, 2.17010142144948]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_021_photonic_linear_algebra_model | Photonic linear algebra model retains throughput-energy gains after system integration assumptions. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.144479 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=20.829587947027253; sig=True; p=4.8531523622703555e-12; ci=[2.0542089634467526, 2.2275398540138878]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_022_optical_boundary_cost | Optical-digital boundary cost can be amortized in hybrid matrix workloads. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.138472 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=26.292185220297224; sig=True; p=6.004065265755071e-13; ci=[2.07146211058278, 2.2041237032326304]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_023_in_memory_compute_model | In-memory compute model reduces data-movement energy enough to raise ECD. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.142484 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=25.401123947785013; sig=True; p=8.182382215679013e-13; ci=[2.0682821605541566, 2.2063937846661537]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_024_endurance_drift_sensitivity | Endurance and drift sensitivity remains within tolerable bounds under projected workloads. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.129510 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=21.20276118531211; sig=True; p=4.1387994458535825e-12; ci=[2.0478009666692647, 2.210987806232976]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |
| exp_025_neuromorphic_temporal | Neuromorphic temporal coding improves joules per event in sparse temporal tasks. | moonshot | baseline_gpu_transformer_bf16_v1 | transformer_inference_small,transformer_inference_medium,transformer_inference_holdout | 10 | 2.124411 | -0.065078 | 6.654404 | -0.140603 | declared_present_but_no_separate_holdout_metric | thr=0.1; effect=23.451148503535606; sig=True; p=1.6758036827876594e-12; ci=[2.0409454906942677, 2.1907395063193116]; ci_ex0=True; quality_ok=True | all_statistical_checks_passed_under_current_pipeline | accepted |

## 3) Integrity Audit

### stubbed_implementations
- Severity: high
- Finding: Mid-term and moonshot families rely on proxy simulators rather than hardware-backed implementations.
- Evidence: simulators/mid_term_simulator.py, simulators/moonshot_simulator.py

### mocked_metrics
- Severity: high
- Finding: Near-term kernels inject random noise and synthetic formulas; no real profiler ingestion in execution path.
- Evidence: src/kernels/quantization.py, src/kernels/sparsity.py, src/kernels/memory_optimization.py, src/kernels/compiler_optimization.py, agents/build/build_agent.py

### dead_code_or_unused_paths
- Severity: medium
- Finding: StatsEvaluator.generate_verdict exists but full pipeline uses StatisticsAgent.evaluate directly.
- Evidence: src/stats_evaluator.py, agents/stats/statistics_agent.py, run_full_program.py

### holdout_leakage_or_missing_holdout_eval
- Severity: critical
- Finding: Benchmark set declares holdout, but ExperimentRunner executes trials only on benchmark_set[0].
- Evidence: src/experiment_runner.py

### acceptance_without_repeated_trials
- Severity: low
- Finding: No acceptance without repeated trials detected in stored records (trials configured as 10).
- Evidence: results/*/experiment.json

### config_only_counted_as_implemented
- Severity: high
- Finding: Some experiment families are config-only wrappers over generic simulators, not bespoke implementations per experiment.
- Evidence: experiments/**/*.yaml, agents/build/build_agent.py

### metrics_collected_but_ignored_in_verdicts
- Severity: high
- Finding: Verdict pipeline primarily uses ecd_improvement, significance, CI, quality_ok; several collected metrics do not affect decision directly.
- Evidence: agents/stats/statistics_agent.py, results/*/experiment.json

## 4) Top 5 Credible Wins (One-Page Summaries)

### 1. exp_003_int4_static_quant_sweep

Summary:
- Horizon: near_term
- Hypothesis: INT4 static quantization sweep can improve ECD with acceptable quality floor enforcement.
- Baseline: baseline_gpu_transformer_bf16_v1
- Benchmarks declared: transformer_inference_small, transformer_inference_medium, transformer_inference_holdout

Measured Outcome:
- Verdict: accepted
- ECD delta: 0.560294
- Quality delta: -0.016979
- Latency delta: -17.965729 ms
- Energy delta: -0.112581 J

Decision Trace:
- Threshold: 0.1
- Effect size: 9.310099409594297
- Significant: True (p=6.373742469345318e-09)
- CI: [0.5111893821265174, 0.6094356408234315] (excludes zero=True)
- Quality gate: True

Credibility Assessment:
- Practical value: high for software-only optimization pathways in existing stack.
- Reproducibility: medium in current form due to synthetic metrics and random noise injection.
- External validity: medium-low until independent holdout scoring and real hardware telemetry are wired in.
- Analyst note: Higher practical value due to near-term path and reusable kernel scaffolding; credibility constrained by synthetic metrics and missing independent holdout scoring.

Actionable Next Step:
- Replace synthetic trial executor with real benchmark harness for this family and re-run dev/validation/holdout separately.

### 2. exp_002_token_pruning

Summary:
- Horizon: near_term
- Hypothesis: Dynamic token pruning improves energy efficiency >=20% with bounded quality loss.
- Baseline: baseline_gpu_transformer_bf16_v1
- Benchmarks declared: transformer_inference_small, transformer_inference_medium, transformer_inference_holdout

Measured Outcome:
- Verdict: accepted
- ECD delta: 0.380232
- Quality delta: -0.046929
- Latency delta: -14.617163 ms
- Energy delta: -0.091552 J

Decision Trace:
- Threshold: 0.1
- Effect size: 4.4149560953458336
- Significant: True (p=3.982369420329183e-06)
- CI: [0.30860864336259913, 0.45677038902373746] (excludes zero=True)
- Quality gate: True

Credibility Assessment:
- Practical value: high for software-only optimization pathways in existing stack.
- Reproducibility: medium in current form due to synthetic metrics and random noise injection.
- External validity: medium-low until independent holdout scoring and real hardware telemetry are wired in.
- Analyst note: Higher practical value due to near-term path and reusable kernel scaffolding; credibility constrained by synthetic metrics and missing independent holdout scoring.

Actionable Next Step:
- Replace synthetic trial executor with real benchmark harness for this family and re-run dev/validation/holdout separately.

### 3. exp_006_token_pruning_threshold_sweep

Summary:
- Horizon: near_term
- Hypothesis: Token pruning threshold sweep reduces energy per task by at least 20% with bounded quality loss.
- Baseline: baseline_gpu_transformer_bf16_v1
- Benchmarks declared: transformer_inference_small, transformer_inference_medium, transformer_inference_holdout

Measured Outcome:
- Verdict: accepted
- ECD delta: 0.380232
- Quality delta: -0.046929
- Latency delta: -14.617163 ms
- Energy delta: -0.091552 J

Decision Trace:
- Threshold: 0.1
- Effect size: 4.4149560953458336
- Significant: True (p=3.982369420329183e-06)
- CI: [0.3124419900013257, 0.44889042914679494] (excludes zero=True)
- Quality gate: True

Credibility Assessment:
- Practical value: high for software-only optimization pathways in existing stack.
- Reproducibility: medium in current form due to synthetic metrics and random noise injection.
- External validity: medium-low until independent holdout scoring and real hardware telemetry are wired in.
- Analyst note: Higher practical value due to near-term path and reusable kernel scaffolding; credibility constrained by synthetic metrics and missing independent holdout scoring.

Actionable Next Step:
- Replace synthetic trial executor with real benchmark harness for this family and re-run dev/validation/holdout separately.

### 4. exp_004_compiler_fusion

Summary:
- Horizon: near_term
- Hypothesis: Kernel fusion reduces p95 latency by >=10% with semantic equivalence.
- Baseline: baseline_gpu_transformer_bf16_v1
- Benchmarks declared: transformer_inference_small, transformer_inference_medium, transformer_inference_holdout

Measured Outcome:
- Verdict: accepted
- ECD delta: 0.227484
- Quality delta: 0.000000
- Latency delta: -8.451146 ms
- Energy delta: -0.052829 J

Decision Trace:
- Threshold: 0.1
- Effect size: 5.10436044822142
- Significant: True (p=1.1783921921470223e-06)
- CI: [0.1895792809695553, 0.26167035145671635] (excludes zero=True)
- Quality gate: True

Credibility Assessment:
- Practical value: high for software-only optimization pathways in existing stack.
- Reproducibility: medium in current form due to synthetic metrics and random noise injection.
- External validity: medium-low until independent holdout scoring and real hardware telemetry are wired in.
- Analyst note: Higher practical value due to near-term path and reusable kernel scaffolding; credibility constrained by synthetic metrics and missing independent holdout scoring.

Actionable Next Step:
- Replace synthetic trial executor with real benchmark harness for this family and re-run dev/validation/holdout separately.

### 5. exp_008_kernel_fusion_loop

Summary:
- Horizon: near_term
- Hypothesis: Iterative kernel fusion loop reduces p95 latency by at least 10%.
- Baseline: baseline_gpu_transformer_bf16_v1
- Benchmarks declared: transformer_inference_small, transformer_inference_medium, transformer_inference_holdout

Measured Outcome:
- Verdict: accepted
- ECD delta: 0.227484
- Quality delta: 0.000000
- Latency delta: -8.451146 ms
- Energy delta: -0.052829 J

Decision Trace:
- Threshold: 0.1
- Effect size: 5.10436044822142
- Significant: True (p=1.1783921921470223e-06)
- CI: [0.19372121402467504, 0.2632513599168754] (excludes zero=True)
- Quality gate: True

Credibility Assessment:
- Practical value: high for software-only optimization pathways in existing stack.
- Reproducibility: medium in current form due to synthetic metrics and random noise injection.
- External validity: medium-low until independent holdout scoring and real hardware telemetry are wired in.
- Analyst note: Higher practical value due to near-term path and reusable kernel scaffolding; credibility constrained by synthetic metrics and missing independent holdout scoring.

Actionable Next Step:
- Replace synthetic trial executor with real benchmark harness for this family and re-run dev/validation/holdout separately.

## 5) Gaps and Next Work

- Replace synthetic metric generation with real benchmark harness integration (GPU telemetry, power, latency traces).
- Execute dev/validation/holdout as independent scored passes and gate acceptance on explicit holdout metrics.
- Unify verdict logic so all configured constraints (latency/energy/complexity/transfer) are mandatory in code.
- Add per-family bespoke implementations for mid-term and moonshot experiments instead of shared generic simulator outputs.
- Add reproducibility hardening: pinned environments, artifact hashing for results/trials, deterministic replay checks.