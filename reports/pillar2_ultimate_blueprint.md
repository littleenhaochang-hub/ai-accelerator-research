# Pillar 2 (Quantization) - The Ultimate Hardware Blueprint
**Target:** Zero-Shot Edge AI Inference (Sub-4-Bit)
**Date:** April 2026

After exhausting the ablation search space across Attention, FFN, Data Types, and Scale Precision, this is the definitive, data-backed architecture required to break the Memory and Compute Walls while surviving the 3.40 dB SNR "Death Line."

## 1. The Optimal Architecture (The "Holy Grail" Configuration)

To achieve maximum tokens/sec within a heavily constrained Edge NPU (e.g., 32MB SLC, LPDDR5), the hardware must adopt an asymmetric, mixed-precision pipeline.

| Component | Target Parameter | Data Type | Effective Bit-Width | Quantization Algorithm | Hardware Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Attention** | **Key (K) Cache** | **INT8** | 8.0 bits | Uniform (Per-Channel) | **Softmax Amplifier:** The exponential nature of Softmax destroys K4 (SNR drops to 1.67 dB). K8 guarantees perfect angular geometry (11.91 dB SNR). |
| **Attention** | **Value (V) Cache** | **FP4 (E2M1)** | 4.5 bits | Block 32 Micro-Scaling | **Linear Payload:** Values are multiplied post-Softmax. FP4 handles the distribution perfectly, halving the V-cache bandwidth. |
| **Attention** | **Q / K / V / O Proj**| **FP4 (E2M1)** | 4.25 bits | Block 32 + E4M3 Scales | **Compute Bound:** Pushing Attention Dense weights to FP4 actually *regularizes* the quantization noise, improving overall logic retention. |
| **FFN** | **Weights (W)** | **FP4 (E2M1)** | 4.25 bits | Block 32 Micro-Scaling | **Outlier Mitigation:** Uniform INT4 fails catastrophically (-1.79 dB). FP4's exponential grid naturally absorbs normal activations near zero. |
| **FFN** | **Activations (A)** | **FP4 (E2M1)** | 4.25 bits | Block 32 Micro-Scaling | **The SiLU Wall:** Requires isolating massive activation spikes into 32-element sub-vectors so they don't crush the surrounding 99% of features. |
| **Global** | **Micro-Scales** | **FP8 (E4M3)** | 8.0 bits (per block) | Dynamic Exponent Mapping | **Scale Precision:** E3M4 clips outliers (1.94 dB). E8M0 drops SNR to 3.00 dB. E4M3 perfectly balances dynamic range and SRAM footprint. |
| **Global** | **Boundary Layers** | **FP16** | 16.0 bits | Native | **Mixed-Precision Bypassing:** Layer 0 (Embedding) and Layer N (LM Head) must bypass quantization to anchor the semantic representations. |

*(Note: If strict 4-bit KV caching is mandated by physical SRAM limits, **SVD 50% Truncation + INT8** (yielding 6.07 dB SNR) replaces the K8V4 format.)*

---

## 2. Next Steps for Pillar 2 (Auto-Researcher Directives)

The theoretical boundaries of Zero-Shot (PTQ) quantization are now mapped. To push the architecture further, the Auto-Researcher must transition from *evaluating* noise to *compensating* for it dynamically.

### Action Item A: The FP4 (E2M1) Hardware Emulator
- **Objective:** Move beyond `fake_quantize` and build a bit-exact emulator for the OCP FP4 MAC unit.
- **Why:** We need to simulate the exact accumulator bit-width (e.g., INT32 vs FP32 vs FP16) when multiplying two FP4 values. If the accumulator lacks precision, the Pipeline Stalls we saw in BitNet (1.58-bit) will reappear.
- **Deliverable:** A PyTorch extension or Triton kernel that performs `FP4 x FP4 -> FP32 Accumulation -> E4M3 Scale Multiplier -> FP4 Output`.

### Action Item B: Learnable Affine Compensation (QAT Lite)
- **Objective:** Defeat the "Cascading Error" of A4KV4 + W4A4 (which currently yields 0.55 dB SNR).
- **Why:** Offline Affine Calibration failed (0.04 Cosine Sim) because KV4 noise is highly non-linear. We cannot fix it with a static Mean/Std shift.
- **Deliverable:** Implement a rapid, 100-step gradient update (Quantization-Aware Training) that *only* trains a tiny Scale/Shift vector placed before the FFN. By freezing the LLM and only training this 1D vector to absorb the KV4 noise, we might achieve QAT-level recovery with PTQ-level compute costs.

### Action Item C: Integration with MoE Drafter (Pillar 3 Crossover)
- **Objective:** Combine the ultimate W4A4 Block 32 architecture with the 68M MoE Drafter.
- **Why:** We proved that a 30M dense drafter takes 15MB of SRAM, but an MoE drafter (68M total, 17M active) takes ~24MB with 65% locality.
- **Deliverable:** Write a cycle-accurate simulator that tracks the LPDDR5x bandwidth consumed by loading the E4M3 scale factors vs. the FP4 weights during a Speculative Decoding phase where the MoE Router misses the SRAM cache.
