# Token Pruning Boundary Conditions

Generated: 2026-03-27T16:04:59.231204Z

Telemetry mode: ACE_DIRECT_POWER_WATTS=185.0 direct override to isolate regime behavior under current environment

Shared executor note: exp_002_token_pruning and exp_006_token_pruning_threshold_sweep both route through the same default PruningConfig() executor in BuildAgent, so boundary behavior is effectively family-level in the current implementation.

## exp_002_token_pruning

### 1) Regime map
- seq_len: [(64, 92.2344, 'positive'), (128, 109.6115, 'positive'), (192, 24.1559, 'positive'), (256, 9.4798, 'positive'), (384, 2.5259, 'positive'), (512, 0.8206, 'positive'), (768, -0.3461, 'negative'), (1024, -0.6281, 'negative')]
- batch: [(1, 101.4389, 'positive'), (2, 20.3558, 'positive'), (3, 6.5685, 'positive'), (4, 2.4635, 'positive'), (6, -0.0535, 'neutral'), (8, -0.6258, 'negative')]
- hidden: [(512, 121.0979, 'positive'), (1024, 113.2185, 'positive'), (1536, 111.552, 'positive'), (2048, 111.9529, 'positive'), (3072, 106.148, 'positive'), (4096, 97.3566, 'positive')]
- layers: [(8, 97.7135, 'positive'), (12, 111.7688, 'positive'), (16, 109.4869, 'positive'), (24, 113.0737, 'positive'), (32, 118.7226, 'positive'), (48, 114.2652, 'positive'), (64, 106.5496, 'positive')]

### 2) Breakpoint analysis
- Dominant variable: seq_len
- Effect strengths: {'seq_len': 110.2395952044943, 'batch': 102.06476661017588, 'hidden': 23.74139407773562, 'layers': 21.009098548392814}
- Breakpoints: {'seq_len': {'cross_zero_point': {'from_value': 512, 'to_value': 768, 'from_ecd': 0.8205589575803912, 'to_ecd': -0.34611298807606605}, 'cross_acceptance_point': {'from_value': 512, 'to_value': 768, 'from_ecd': 0.8205589575803912, 'to_ecd': -0.34611298807606605}}, 'batch': {'cross_zero_point': {'from_value': 4, 'to_value': 6, 'from_ecd': 2.4634550950783227, 'to_ecd': -0.0535031357144458}, 'cross_acceptance_point': {'from_value': 4, 'to_value': 6, 'from_ecd': 2.4634550950783227, 'to_ecd': -0.0535031357144458}}, 'hidden': {'cross_zero_point': None, 'cross_acceptance_point': None}, 'layers': {'cross_zero_point': None, 'cross_acceptance_point': None}}
- Actual tiers: [('development', 118.116, 1.4615, 702169.34), ('validation', 3.1253, 7.8327, 326974.18), ('holdout', -0.6396, 26.4907, 270610.27)]

### 3) Mechanism report
- {'scheduler_effects': {'evidence': 'ECD decays as runtime grows because candidate_qat uses measured runtime_ms * energy_joules, and with direct power override energy scales linearly with runtime, creating near-quadratic penalty in runtime.', 'seq_runtime_growth_ms': [(64, 1.6871691672753917), (128, 1.522631944782107), (192, 3.1798366668024554), (256, 4.915703333709745), (384, 8.485616109202157), (512, 11.785061111125591), (768, 20.026055554909462), (1024, 26.116014999206527)], 'batch_runtime_growth_ms': [(1, 1.6263836100430733), (2, 3.444345834355368), (3, 5.782336110941186), (4, 8.549059167368492), (6, 16.347039166774064), (8, 25.996942499518305)]}, 'memory_effects': {'evidence': 'Memory peak increases with larger sequence/batch, but hidden size is currently not wired into measured workload size, so memory pressure is mostly driven by seq_len and batch.', 'seq_memory_mb': [(64, 0.00025177001953125), (128, 0.00025177001953125), (192, 0.00029754638671875), (256, 0.00029754638671875), (384, 0.00029754638671875), (512, 0.00029754638671875), (768, 0.00032806396484375), (1024, 0.00032806396484375)], 'batch_memory_mb': [(1, 0.00025177001953125), (2, 0.00029754638671875), (3, 0.00029754638671875), (4, 0.00029754638671875), (6, 0.00029754638671875), (8, 0.00029754638671875)], 'hidden_memory_mb': [(512, 0.00025177001953125), (1024, 0.00025177001953125), (1536, 0.00025177001953125), (2048, 0.00025177001953125), (3072, 0.00025177001953125), (4096, 0.00025177001953125)]}, 'pruning_overhead': {'evidence': 'Pruning latency improvement and pruning ratio stay almost flat across depth because avg_pruning_ratio is target_ratio * floor(0.75 * layers)/layers, while hidden size is unused in prune_tokens.', 'layer_latency_improvement': [(8, 0.12749999999999992), (12, 0.12749999999999992), (16, 0.12749999999999992), (24, 0.12749999999999992), (32, 0.12749999999999992), (48, 0.12749999999999992), (64, 0.12749999999999992)], 'layer_pruning_ratio': [(8, 0.15000000000000002), (12, 0.15000000000000002), (16, 0.15000000000000002), (24, 0.15000000000000002), (32, 0.15000000000000002), (48, 0.15000000000000002), (64, 0.15000000000000002)], 'hidden_ecd': [(512, 121.09794647908704), (1024, 113.21853237232236), (1536, 111.55201573725573), (2048, 111.95294907085669), (3072, 106.14802211848652), (4096, 97.35655240135142)]}}

### 4) Result classification
- useful in bounded regime

## exp_006_token_pruning_threshold_sweep

### 1) Regime map
- seq_len: [(64, 117.5549, 'positive'), (128, 111.8709, 'positive'), (192, 23.7451, 'positive'), (256, 9.8931, 'positive'), (384, 2.76, 'positive'), (512, 0.7945, 'positive'), (768, -0.3206, 'negative'), (1024, -0.6198, 'negative')]
- batch: [(1, 99.9498, 'positive'), (2, 22.0352, 'positive'), (3, 6.1993, 'positive'), (4, 2.1689, 'positive'), (6, -0.0817, 'neutral'), (8, -0.6309, 'negative')]
- hidden: [(512, 115.8523, 'positive'), (1024, 110.5824, 'positive'), (1536, 112.4134, 'positive'), (2048, 113.5836, 'positive'), (3072, 111.4744, 'positive'), (4096, 101.7012, 'positive')]
- layers: [(8, 101.6479, 'positive'), (12, 97.4618, 'positive'), (16, 115.9354, 'positive'), (24, 118.8704, 'positive'), (32, 110.5814, 'positive'), (48, 113.9832, 'positive'), (64, 110.948, 'positive')]

### 2) Breakpoint analysis
- Dominant variable: seq_len
- Effect strengths: {'seq_len': 118.1746597107309, 'batch': 100.58067536502772, 'hidden': 14.151089350110126, 'layers': 21.40856703702329}
- Breakpoints: {'seq_len': {'cross_zero_point': {'from_value': 512, 'to_value': 768, 'from_ecd': 0.7945073843602021, 'to_ecd': -0.32058425336495877}, 'cross_acceptance_point': {'from_value': 512, 'to_value': 768, 'from_ecd': 0.7945073843602021, 'to_ecd': -0.32058425336495877}}, 'batch': {'cross_zero_point': {'from_value': 4, 'to_value': 6, 'from_ecd': 2.1688612352259544, 'to_ecd': -0.0817326065786196}, 'cross_acceptance_point': {'from_value': 4, 'to_value': 6, 'from_ecd': 2.1688612352259544, 'to_ecd': -0.0817326065786196}}, 'hidden': {'cross_zero_point': None, 'cross_acceptance_point': None}, 'layers': {'cross_zero_point': None, 'cross_acceptance_point': None}}
- Actual tiers: [('development', 111.3113, 1.5126, 680741.35), ('validation', 3.3129, 7.6648, 334263.78), ('holdout', -0.6424, 26.5989, 269542.84)]

### 3) Mechanism report
- {'scheduler_effects': {'evidence': 'ECD decays as runtime grows because candidate_qat uses measured runtime_ms * energy_joules, and with direct power override energy scales linearly with runtime, creating near-quadratic penalty in runtime.', 'seq_runtime_growth_ms': [(64, 1.4665955551511918), (128, 1.500326666326954), (192, 3.20205916624319), (256, 4.8213797222059736), (384, 8.204756665751725), (512, 11.871518888316738), (768, 19.317476111084236), (1024, 25.809268333190023)], 'batch_runtime_growth_ms': [(1, 1.6081883327691078), (2, 3.320368611194782), (3, 5.932486667006742), (4, 9.040853333580243), (6, 16.608179166602593), (8, 26.17713388816709)]}, 'memory_effects': {'evidence': 'Memory peak increases with larger sequence/batch, but hidden size is currently not wired into measured workload size, so memory pressure is mostly driven by seq_len and batch.', 'seq_memory_mb': [(64, 0.00025177001953125), (128, 0.00025177001953125), (192, 0.00029754638671875), (256, 0.00029754638671875), (384, 0.00029754638671875), (512, 0.00029754638671875), (768, 0.00032806396484375), (1024, 0.00032806396484375)], 'batch_memory_mb': [(1, 0.00025177001953125), (2, 0.00029754638671875), (3, 0.00029754638671875), (4, 0.00029754638671875), (6, 0.00029754638671875), (8, 0.00029754638671875)], 'hidden_memory_mb': [(512, 0.00025177001953125), (1024, 0.00025177001953125), (1536, 0.00025177001953125), (2048, 0.00025177001953125), (3072, 0.00025177001953125), (4096, 0.00025177001953125)]}, 'pruning_overhead': {'evidence': 'Pruning latency improvement and pruning ratio stay almost flat across depth because avg_pruning_ratio is target_ratio * floor(0.75 * layers)/layers, while hidden size is unused in prune_tokens.', 'layer_latency_improvement': [(8, 0.12749999999999992), (12, 0.12749999999999992), (16, 0.12749999999999992), (24, 0.12749999999999992), (32, 0.12749999999999992), (48, 0.12749999999999992), (64, 0.12749999999999992)], 'layer_pruning_ratio': [(8, 0.15000000000000002), (12, 0.15000000000000002), (16, 0.15000000000000002), (24, 0.15000000000000002), (32, 0.15000000000000002), (48, 0.15000000000000002), (64, 0.15000000000000002)], 'hidden_ecd': [(512, 115.85227518516751), (1024, 110.58235596908578), (1536, 112.41336194431487), (2048, 113.58359007790759), (3072, 111.47437838774371), (4096, 101.70118583505739)]}}

### 4) Result classification
- useful in bounded regime
