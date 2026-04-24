# Hardware GEMV (Vector-MAC) Engine for LLM Decoding

## Background
Standard NPU architectures rely heavily on dense 2D Systolic Arrays designed for Matrix-Matrix Multiplication (GEMM), which are highly efficient during the Prefill phase. However, during the Autoregressive Decoding phase (batch size = 1), the operation devolves into Matrix-Vector Multiplication (GEMV). Feeding a vector into a massive 2D systolic array results in catastrophic underutilization (often <5%), crippling generation speed (Tokens Per Second).

## Hardware Simulation
We simulated the latency of decoding tokens using a standard dense Systolic Array versus a dedicated 1D Vector-MAC (VMAC) Engine (`gemv_decode_hw_sim.py`).
- **Systolic Array Decode Latency:** 16777.22 ms (for 2048 tokens, d_model=4096)
- **Dedicated VMAC Decode Latency:** 838.86 ms
- **Speedup:** 20.00x

## Architectural Proposal
We propose a **"Heterogeneous Prefill-Decode Architecture"** for Edge NPUs. Instead of forcing all operations through the 2D Systolic Array, the NPU should integrate a parallel set of **1D Vector-MAC (VMAC) Engines** located directly adjacent to the SRAM banks. During Prefill, the NPU routes data to the Systolic Array. During Decode, it instantly switches to the VMAC engines, ensuring 100% compute utilization and massively accelerating the single-batch generation speed crucial for real-time Agentic AI.
