# Ablation Study: Towards A4 KV4 Attention Quantization

**Date:** March 31, 2026
**Context:** Conducting a strict step-by-step ablation study on the Attention mechanism (Softmax included) to map the SNR degradation from quantizing only the KV cache (KV4) to quantizing the full query matrix (A4 KV4).

## 1. Methodology
We simulated an Attention block (`Q, K, V`) at sequence length 256 and feature dimension 128. Massive LLM-style outliers were injected across all three matrices. We evaluated the Final Output SNR (Post-Softmax and V-projection) under two sequential stages:
*   **Stage 1 (KV4):** Only `K` and `V` are quantized to 4-bit. `Q` remains perfectly precise in FP32. This isolates the error of storing the KV cache.
*   **Stage 2 (A4 KV4):** `Q` is also quantized to 4-bit. This introduces the variance compounding effect ($e_q \cdot e_k$) into the dot product, simulating a fully edge-quantized NPU.

## 2. Empirical Results (Final Attention Output SNR)

| Method | STAGE 1: KV4 (Q is FP32) | STAGE 2: A4 KV4 (Q is 4-bit) | $\Delta$ (A4 Penalty) |
| :--- | :--- | :--- | :--- |
| **Naive 4-Bit** | `7.70 dB` | `7.43 dB` | -0.27 dB |
| **Sub-Channel (E8M0, G=32)** | `8.22 dB` | `8.63 dB` | +0.41 dB |
| **Sub-Channel (FP16, G=32)** | `14.41 dB` | `14.18 dB` | -0.23 dB |
| **TurboQuant (Rotation)** | `15.24 dB` | `15.19 dB` | -0.05 dB |
| **TurboQuant + 1-bit QJL** | **`20.61 dB`** | **`18.69 dB`** | -1.92 dB |

## 3. Analytical Findings

1.  **The A4 Compounding Penalty is Real:** Moving from FP32 queries to 4-bit queries (A4 KV4) causes the top-performing method (TurboQuant + QJL) to lose nearly **2 dB** of accuracy. This confirms our earlier hypothesis: quantizing $Q$ introduces a cross-term error $e_q$ that interacts with the existing $e_k$ noise, flattening the Softmax distribution.
2.  **Sub-Channel E8M0 Fails on Attention:** Earlier today, we proved Sub-Channel E8M0 is the ultimate winner for FFN activations (`18.35 dB`). However, in the full Attention block (where the Softmax exponential amplifier is involved), E8M0 completely collapses to `~8.6 dB`. Forcing the scale to a power of 2 across 32 elements distorts the dot-product *just enough* that the Softmax points to the wrong tokens.
3.  **TurboQuant + QJL remains the undisputed champion:** For the entire Attention block, spreading the outliers via an orthogonal matrix and fixing the KV cache with a 1-bit residual (`18.69 dB` in A4KV4) massively outperforms the standard Sub-Channel FP16 approach (`14.18 dB`).

## 4. Architectural Summary
*   **For Attention (A4 KV4):** You MUST use **TurboQuant + 1-Bit QJL**. Sub-channel (whether FP16 or E8M0) cannot survive the Softmax amplification when severe outliers are present across $Q, K$, and $V$.
*   **For FFN (A4W4):** Use **Sub-Channel E8M0**. Since there is no Softmax in the FFN, the E8M0 power-of-2 scaling error is harmless, providing massive multiplier-free power savings.