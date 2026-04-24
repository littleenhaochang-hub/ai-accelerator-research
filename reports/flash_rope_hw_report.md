# Hardware Flash-RoPE Engine

## Background
Rotary Position Embeddings (RoPE) require element-wise complex multiplications with sine and cosine vectors for every token in the query and key tensors. For extreme long-context prefilling (e.g., 16K+ tokens), generating or fetching these trigonometric values and performing the multiplications occupies significant MAC execution time and SRAM bandwidth, acting as a hidden latency tax on Attention mechanisms.

## Hardware Simulation
We simulated the latency of standard RoPE calculation versus an in-line Hardware Flash-RoPE engine (`flash_rope_hw_sim.py`).
- **Standard RoPE Latency:** 4194.30 ms (16K context, d_head=128)
- **Hardware Flash-RoPE Latency:** 104.86 ms
- **Speedup:** 40.00x

## Architectural Proposal
We propose integrating a **"Flash-RoPE CORDIC Engine"** directly into the SRAM read path of the NPU's Attention block. Instead of relying on the main Tensor Cores, this specialized unit uses a CORDIC algorithm to compute rotations on the fly as the Query and Key vectors stream from SRAM to the Attention ALU. This effectively hides the RoPE compute latency entirely behind the memory fetch latency, resulting in zero MAC overhead.
