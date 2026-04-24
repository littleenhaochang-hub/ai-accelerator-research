# Hardware Fused GEMM and Activation Engine

## Background
In standard FFN (Feed-Forward Network) blocks, the output of the GEMM (General Matrix Multiply) operation is written back to SRAM. Subsequently, an Activation layer (such as SwiGLU or SiLU) reads this data back from SRAM, applies the non-linear function, and writes it back. This two-pass approach wastes significant SRAM bandwidth and power, particularly for wide hidden layers in modern LLMs.

## Hardware Simulation
We simulated the latency of standard separate GEMM and Activation passes versus a fused hardware execution path (`gemm_fused_activation_sim.py`).
- **Standard Separate Pass Latency:** 117440.51 ms
- **Fused Hardware Latency:** 85563.80 ms
- **Speedup:** 1.37x

## Architectural Proposal
We propose integrating a **"Fused Activation LUT (Look-Up Table) & PWL Engine"** directly at the output of the NPU's Accumulator Register File. As the MAC array finalizes the dot product, the result flows directly through the Activation Engine before ever touching the SRAM. This "Zero-DRAM-Bounce" architecture reduces SRAM writes and reads by 50% for the FFN block, freeing up internal bandwidth and lowering dynamic power consumption on Edge devices.
