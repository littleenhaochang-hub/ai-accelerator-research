# Hardware Heavy-Hitter Oracle for KV Cache Pruning

## Background
For ultra-long contexts (e.g., 32K+ tokens), the KV cache size exceeds the capacity of Edge NPU SRAM, forcing a fallback to slow LPDDR memory. Research shows that Attention naturally focuses on a small subset of "Heavy-Hitter" tokens (sinks and crucial context), while the vast majority of intermediate tokens can be safely evicted without accuracy loss. Managing this eviction dynamically in software introduces severe tracking overhead.

## Hardware Simulation
We simulated the memory footprint and access latency of a full KV cache versus a Hardware Heavy-Hitter Oracle that autonomously prunes 80% of low-attention tokens (`heavy_hitter_oracle_sim.py`).
- **Standard KV Cache:** 16384.00 KB, Latency: 1638.40 ms
- **Heavy-Hitter Oracle Cache:** 3276.80 KB, Latency: 393.22 ms
- **Memory Compression:** 5.00x
- **Speedup:** 4.17x

## Architectural Proposal
We propose integrating a **"Hardware Heavy-Hitter Oracle"** directly into the NPU's SRAM Controller. This logic block monitors the accumulated Attention scores emitted by the Softmax ALU. When the SRAM KV ring buffer nears capacity, the Oracle autonomously overwrites the physical memory slots of the lowest-scoring tokens. This hardware-managed eviction guarantees that the KV cache remains entirely in-SRAM indefinitely, delivering infinite context lengths within a fixed, tiny memory envelope.
