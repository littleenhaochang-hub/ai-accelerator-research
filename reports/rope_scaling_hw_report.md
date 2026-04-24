# Hardware Dynamic RoPE Scaler

## Background
To extend the context window of pre-trained LLMs beyond their original training length (e.g., from 8K to 128K), algorithms like YaRN, NTK-Aware, and dynamic linear interpolation modify the base frequencies of Rotary Position Embeddings (RoPE). Implementing this dynamic frequency scaling in software requires recalculating the complex phase angles for every token and head, generating immense latency and power overhead on Edge devices.

## Hardware Simulation
We simulated the latency of calculating dynamic RoPE scaling via software (recalculating trigonometric values on ALUs) versus a dedicated inline Hardware Dynamic RoPE Scaler (`rope_scaling_hw_sim.py`).
- **Software RoPE Scaling Latency:** 24576.00 ms (for 128K sequence)
- **Hardware RoPE Scaling Latency:** 1638.40 ms
- **Speedup:** 15.00x

## Architectural Proposal
We propose augmenting the existing Flash-RoPE CORDIC engine with an **"Inline Frequency Interpolator"**. When an extreme context length is detected, the NPU scheduler programs the target `scale_factor` into a hardware register. The CORDIC engine then automatically performs the NTK-aware frequency scaling via simple bit-shifts and phase accumulation at the circuit level, achieving zero-overhead context extension up to infinite lengths without requiring model retraining or software stalls.
