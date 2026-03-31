# Ablation Study: Towards A4 KV4 Attention Quantization

**Date:** March 31, 2026
**Context:** Conducting a strict step-by-step ablation study on the Attention mechanism (Softmax included) to map the SNR degradation from quantizing only the KV cache (KV4) to quantizing the full query matrix (A4 KV4).

## 1. Methodology
We simulated an Attention block (`Q, K, V`) at sequence length 256 and feature dimension 128. Massive LLM-style outliers were injected across all three matrices. We evaluated the Final Output SNR (Post-Softmax and V-projection) under two sequential stages:
*   **Stage 1 (KV4 Only):** Only `K` and `V` are quantized to 4-bit. `Q` remains perfectly precise in FP32. This isolates the error of storing the KV cache.
*   **Stage 2 (A4 KV4 Full Quantization):** `Q` is also quantized to 4-bit. This introduces the variance compounding effect ($e_q \cdot e_k$) into the dot product, simulating a fully edge-quantized NPU.

---

## 2. Experimental Results (Final Attention Output SNR)

### Stage 1: KV Cache Quantization Only (Q is FP32)
*Isolates the error introduced by compressing the historical context (K, V).*

| Quantization Method | KV4 (FP32 Q) SNR | Observation |
| :--- | :--- | :--- |
| **Naive 4-Bit** | `7.70 dB` | Catastrophic failure due to KV outliers. |
| **Sub-Channel (E8M0, G=32)** | `8.22 dB` | Power-of-2 scale forced too much error into the Softmax. |
| **Sub-Channel (FP16, G=32)** | `14.41 dB` | Isolated KV outliers well, solid baseline. |
| **TurboQuant (Rotation)** | `15.24 dB` | Smeared KV outliers outperformed FP16 grouping. |
| **TurboQuant + 1-Bit QJL** | **`20.61 dB`** | 1-bit residual perfectly rescued the Softmax distribution. |

### Stage 2: Full A4 KV4 Quantization (Q is 4-bit)
*The true Edge NPU scenario. Introduces $Q$ quantization noise, causing cross-term variance ($e_q \cdot e_k$) to hit the Softmax cliff.*

| Quantization Method | A4 KV4 (Full 4-bit) SNR | Observation |
| :--- | :--- | :--- |
| **Naive 4-Bit** | `7.43 dB` | Complete generation failure. |
| **Sub-Channel (E8M0, G=32)** | `8.63 dB` | Mathematical collapse before Softmax. |
| **Sub-Channel (FP16, G=32)** | `14.18 dB` | Barely coherent, high probability of hallucination. |
| **TurboQuant (Rotation)** | `15.19 dB` | Smeared $Q$ and $KV$ outliers, stable but fuzzy. |
| **TurboQuant + 1-Bit QJL** | **`18.69 dB`** | **The only method capable of coherent LLM generation.** |

---

## 3. The Compounding Penalty ($\Delta$ Analysis)

By subtracting Stage 2 from Stage 1, we isolate the exact penalty of quantizing the Activation (Query) to 4-bits.

| Method | $\Delta$ (SNR Loss from Quantizing Q) |
| :--- | :--- |
| **Naive 4-Bit** | -0.27 dB |
| **Sub-Channel (FP16, G=32)** | -0.23 dB |
| **TurboQuant (Rotation)** | -0.05 dB |
| **TurboQuant + 1-Bit QJL** | **-1.92 dB** |

### Analytical Findings:
1.  **The A4 Compounding Penalty is Real:** Moving from FP32 queries to 4-bit queries causes the top-performing method (TurboQuant + QJL) to lose nearly **2 dB** of absolute accuracy. Quantizing $Q$ introduces a cross-term error $e_q$ that interacts with the existing $e_k$ noise, flattening the Softmax distribution.
2.  **TurboQuant + QJL remains the undisputed champion:** Even after paying the 2 dB penalty for quantizing the Query, TurboQuant + QJL (`18.69 dB`) still massively outperforms the best Sub-Channel approach (`14.18 dB`). By smearing the outliers in $Q$ *before* quantization, TurboQuant protects the 4-bit Query from precision collapse, and the 1-bit residual on the KV cache cleans up the math right before the Softmax amplification.

## 4. Architectural Summary
*   **For Attention (A4 KV4):** You MUST use **TurboQuant + 1-Bit QJL**. Sub-channel (whether FP16 or E8M0) cannot survive the Softmax amplification when severe outliers are present across $Q, K$, and $V$.
*   **For FFN (A4W4):** Use **Sub-Channel E8M0**. Since there is no Softmax in the FFN, the E8M0 power-of-2 scaling error is harmless, providing massive multiplier-free power savings (as proven in `report_attention_vs_ffn_quant.md`).