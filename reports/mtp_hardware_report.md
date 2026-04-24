# Multi-Token Prediction (MTP) Hardware Scheduler

## Background
Following the advancements in DeepSeek-V3, Multi-Token Prediction (MTP) allows a model to predict multiple future tokens simultaneously by reusing the primary hidden states and feeding them through parallel, lightweight projection heads. This eliminates the need for separate draft models (as in Speculative Decoding) while maintaining high acceptance rates.

## Hardware Simulation
We simulated the latency and MAC utilization of a baseline Autoregressive (AR) pipeline versus a Hardware MTP Scheduler with `K=4` depth (`mtp_hardware_sim.py`).
- **Standard AR Latency:** 50.00 s (for 1000 tokens)
- **MTP Hardware Latency:** 24.00 s
- **Speedup:** 2.08x

## Architectural Proposal
To maximize this algorithm at the Edge, we propose integrating a **"Hardware MTP Scheduler"** and **"Parallel Projection ALUs"** directly into the NPU. By physically separating the deep transformer MAC arrays from the shallow MTP projection arrays, the NPU can fetch the memory state once, broadcast it to the parallel MTP ALUs, and instantly generate K speculative tokens without sequential memory stalls. This avoids the area overhead of a Big.LITTLE dual-NPU setup while still doubling the decoding throughput.
