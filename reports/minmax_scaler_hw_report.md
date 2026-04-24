# Hardware Dynamic Min-Max Scaler

## Background
Dynamic quantization per-token or per-channel is crucial for maintaining accuracy in sub-4-bit INT quantization (like W4A4 or KV4). However, doing this dynamically in software requires multiple memory passes: one pass to find the min/max values across the tensor, and a second pass to compute and apply the scale/zero-point. This memory-bound operation stalls the NPU pipeline.

## Hardware Simulation
We simulated the latency of dynamic min-max scaling in software versus an inline hardware scalar (`minmax_scaler_hw_sim.py`).
- **Software Scaling Latency:** 16.38 ms (for 8192 elements)
- **Hardware Inline Scaler Latency:** 0.82 ms
- **Speedup:** 20.00x

## Architectural Proposal
We propose integrating an **"Inline Dynamic Min-Max Scaler"** directly at the SRAM write ports. As activation or KV cache data streams out of the Tensor Core towards the SRAM, the hardware continuously tracks the running min/max. At the end of the block, it instantly computes the scale and zero-point and applies the quantization during the final write cycle. This provides zero-overhead dynamic quantization, resolving the precision vs. memory bandwidth dilemma for Edge NPUs.
