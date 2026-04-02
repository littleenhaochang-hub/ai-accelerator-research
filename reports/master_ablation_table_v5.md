# Master Ablation Unified Data Table: Attention & FFN Quantization
**Target Model:** Qwen2.5-0.5B-Instruct
**Date:** April 2026

To provide a clear, unified view of all configurations tested across the quantization pipeline, this master table maps out the exact precision and mechanisms applied to both the Attention and FFN blocks, along with the resulting model-level metrics.

| Experiment Name | Model Layer Scope | Attn Act | Attn KV | Attn Mechanism | FFN Act | FFN W | FFN Mechanism | SNR (dB) | RMSE | Cosine Sim | Pass Rate | Status / Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0. FP16 Baseline** | All Layers | 16 | 16 | None | 16 | 16 | None | ∞ | 0.000 | 1.000 | 70% | 🟢 Native performance. |
| **1. A8KV8 (Attn Only)** | All Layers | 8 | 8 | Uniform | 16 | 16 | None | 12.40 | 1.210 | 0.952 | 70% | 🟢 Perfect fallback. INT8 absorbs KV outliers. |
| **2. A4KV4 (Attn Only)** | All Layers | 4 | 4 | 1D Hadamard (Feature) | 16 | 16 | None | -0.61 | 9.617 | 0.466 | 0% | 🔴 OOV Collapse. Hadamard noise breaks Softmax. |
| **3. A4KV4 (Attn Only)** | All Layers | 4 | 4 | 2D Hadamard (Tok+Feat) | 16 | 16 | None | -1.36 | 10.500 | 0.358 | 0% | 🔴 Overflow. Sequence length breaks energy bounds. |
| **4. W4A16 (FFN Only)** | All Layers | 16 | 16 | None | 16 | 4 | Block 32 | 8.50 | 2.140 | 0.922 | 75% | 🟢 Logic fully retained. Memory bound resolved. |
| **5. W4A4 Naive (FFN)** | All Layers | 16 | 16 | None | 4 | 4 | Uniform | <0.00 | >10.0 | <0.200 | 0% | 🔴 Catastrophic forgetting. SiLU destroys uniform grid. |
| **6. W4A4 Smooth (FFN)** | All Layers | 16 | 16 | None | 4 | 4 | SmoothQuant (α=0.75) | -0.58 | 9.593 | 0.468 | 0% | 🔴 Fails to smooth SiLU spikes dynamically. |
| **7. W4A4 Block 32 (FFN)** | All Layers | 16 | 16 | None | 4 | 4 | Block 32 Micro-Scaling | 4.24 | 5.511 | 0.797 | 75% | 🟢 **Breakthrough.** Outliers successfully isolated. |
| **8. A8KV8 + W4A4 Fusion** | All Layers | 8 | 8 | Uniform | 4 | 4 | Block 32 | 3.40 | 6.820 | 0.743 | 65% | 🟡 **Hardware Sweet Spot.** Survives "SNR Death Line". |
| **9. A16KV4 + W4A4 Fusion** | All Layers | 16 | 4 | 1D Hadamard | 4 | 4 | Block 32 | 0.55 | 8.429 | 0.542 | 5% | 🔴 Cascading Error. KV4 noise destroys FFN A4. |
| **10. A8KV4 + W4A4 Fusion** | All Layers | 8 | 4 | 1D Hadamard | 4 | 4 | Block 32 | 0.56 | 8.414 | 0.537 | 0% | 🔴 Cascading Error. Attention input bit-width irrelevant. |
| **11. Mixed-Precision FFN** | **Mid Layers (1-22)** | 16 | 16 | None | 4 | 4 | Block 32 | 4.92 | N/A | 0.822 | 70% | 🟢 **Ultimate Solution.** Protecting boundaries restores IQ. |

---

## Future Hardware Direction (Data Type & Scale Precisions)
Based on the table above, the optimal hardware architecture moving forward requires transitioning from **INT4** to **FP4 (E2M1)** to naturally absorb normal activations around zero, while maintaining outliers in the sparse upper range. Furthermore, the FFN Sub-Channel Mechanism (Block 32) must be optimized to use **E8M0** or **E4M3 (FP8)** scaling factors to reduce the SRAM footprint from an effective 4.5 bits down to 4.25 bits.
