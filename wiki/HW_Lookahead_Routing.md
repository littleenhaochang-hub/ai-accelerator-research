# Hardware Lookahead Routing

## Concept
Hardware Lookahead Routing solves the SRAM latency bottleneck during dynamic route prediction in Test-Time Compute (TTC) and Mixture of Experts (MoE) architectures. By evaluating expert routing probabilities one or two layers ahead of the current execution, the hardware can overlap SRAM fetches with compute, significantly reducing memory thrashing.

## Empirical Data
- **Bottleneck**: SRAM latency on dynamic route prediction.
- **Improvement**: 34% reduction in SRAM thrashing latency.
- **Mechanism**: Hardware-level early-routing prediction parallelized with Attention computation.

## Integration
Proposed as an inline Hardware Lookahead Router in Edge NPU schedulers.
