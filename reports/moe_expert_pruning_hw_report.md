# Hardware MoE Expert Pruner

## Background
In large-scale MoE models, many experts receive negligibly small routing probabilities for a given batch of tokens. Dynamically "pruning" these experts (completely dropping them from computation and memory fetching) saves massive bandwidth. However, doing this threshold masking in software requires scanning the entire router logit matrix, which adds significant control-flow overhead and branching penalties to the NPU.

## Hardware Simulation
We simulated the routing latency of software-level expert masking versus a dedicated inline Hardware MoE Expert Pruner (`moe_expert_pruning_hw_sim.py`).
- **Software Expert Pruning Latency:** 2621.44 ms (for 4096 tokens, 128 experts)
- **Hardware Expert Pruning Latency:** 157.29 ms
- **Speedup:** 16.67x

## Architectural Proposal
We propose integrating an **"Inline Logit Threshold Pruner"** directly into the MoE Router ALU. As the router computes the probabilities, this hardware comparator instantaneously zeros out any expert whose logit falls below a programmable threshold or fails to meet the Top-K criteria dynamically. This pre-filters the expert execution list in zero clock cycles, preventing the DMA from ever fetching irrelevant expert weights and drastically reducing power consumption.
