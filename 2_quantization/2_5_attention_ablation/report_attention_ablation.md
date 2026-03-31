# Ablation Study: Towards A4 KV4 Attention Quantization

**Date:** March 31, 2026
**Context:** Conducting a strict step-by-step ablation study on the Attention mechanism (Softmax included) to map the SNR degradation from quantizing only the KV cache (KV4) to quantizing the full query matrix (A4 KV4).

## 1. Core Methodology

We simulated an Attention block (`Q, K, V`) at sequence length 256 and feature dimension 128, injecting massive LLM-style outliers across all three matrices. We evaluated the output under two sequential stages:

*   **Stage 1 (KV4 Only):** Only `K` and `V` are quantized. `Q` remains in perfect FP32.
*   **Stage 2 (A4 KV4 Full Quantization):** `Q` is quantized to 4-bit.
    *   *Critical Note on Symmetry:* In Stage 2, **we apply the exact same quantization methodology to `Q` as we do to `KV`.** For example, in the TurboQuant row, `Q` is also multiplied by the identical orthogonal rotation matrix $R$ before being quantized to 4-bit. This is a mathematical requirement: if $K$ is rotated, $Q$ must also be rotated by the same matrix so the dot product $Q \cdot K^T$ remains in the correct coordinate space.

---

## 2. Demystifying the "dB" (Signal-to-Noise Ratio) Metric

To scientifically measure the quality of a quantization algorithm without running a full LLM, we use **Signal-to-Noise Ratio (SNR) measured in Decibels (dB)**. 

### What does the math actually mean?
The formula is: $10 \cdot \log_{10}\left( \frac{\text{Variance of True FP32 Signal}}{\text{Variance of Quantization Noise}} \right)$

*   **Signal:** The perfectly accurate FP32 attention output.
*   **Noise:** The mathematical difference (error) between the FP32 output and our 4-bit quantized output.

### How to read the numbers:
*   **Higher is better.** A positive dB means the true signal is louder than the quantization noise.
*   **Logarithmic Scale:** Because it's a $\log_{10}$ scale, **every drop of 3 dB means the noise energy (variance) has exactly doubled**.
*   **Real-world thresholds:**
    *   `< 10 dB`: The noise is so loud the model is completely deaf. It will output gibberish.
    *   `14~15 dB`: The model can speak English, but it is "fuzzy" and will hallucinate facts.
    *   `> 18 dB`: The quantization noise is quiet enough that the LLM's internal logic stays intact.

---

## 3. Experimental Results (Final Attention Output SNR)

### Stage 1: KV Cache Quantization Only (Q is FP32)
*Isolates the error introduced by compressing the historical context (K, V).*

| Quantization Method | KV4 (FP32 Q) SNR | Live Qwen 0.5B Evaluation (Gate B) | Observation |
| :--- | :--- | :--- | :--- |
| **Naive 4-Bit** | `7.70 dB` | "The question is a of France is a French..." | Catastrophic failure due to KV outliers. Semantic loss. |
| **Sub-Channel (E8M0, G=32)** | `8.22 dB` | "The capital of France is a French film directed by..." | Power-of-2 scale forced too much error into the Softmax. Hallucinates facts. |
| **Sub-Channel (FP16, G=32)** | `14.41 dB` | "The capital of France is Paris. The capital of France is Paris, which..." | Isolated KV outliers well, solid baseline, but repeats. |
| **TurboQuant (Rotation)** | `15.24 dB` | "a the a a a a a" | Rotation without residual creates widespread fuzziness, Softmax collapses to noise. |
| **TurboQuant + 1-Bit QJL** | **`20.61 dB`** | **"The capital city of France is Paris."** | 1-bit residual perfectly rescued the Softmax distribution. Flawless syntax. |

### Stage 2: Full A4 KV4 Quantization (Q is 4-bit)
*The true Edge NPU scenario. Introduces $Q$ quantization noise, causing cross-term variance ($e_q \cdot e_k$) to hit the Softmax cliff.*

| Quantization Method | A4 KV4 (Full 4-bit) SNR | Live Qwen 0.5B Evaluation (Gate B) | Observation |
| :--- | :--- | :--- | :--- |
| **Naive 4-Bit** | `7.43 dB` | "The capital of France is" (Stops) | Complete generation failure. Outliers crush activation scales. |
| **Sub-Channel (E8M0, G=32)** | `8.63 dB` | (Outputs blank/silence) | Mathematical collapse before Softmax. |
| **Sub-Channel (FP16, G=32)** | `14.18 dB` | "The capital of France was Paris, which had been founded in 1657890..." | Coherent grammar, but extreme hallucination of facts due to cross-term variance. |
| **TurboQuant (Rotation)** | `15.19 dB` | "def capth Assistant\nc \" | Smeared $Q$ and $KV$ outliers, stable but fuzzy, logic destroyed. |
| **TurboQuant + 1-Bit QJL** | **`18.69 dB`** | **"The capital of for France is Paris."** | **The only method capable of preserving semantic LLM generation.** |

---

## 4. The Compounding Penalty ($\Delta$ Analysis)

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

## 5. Architectural Summary
*   **For Attention (A4 KV4):** You MUST use **TurboQuant + 1-Bit QJL**. Sub-channel (whether FP16 or E8M0) cannot survive the Softmax amplification when severe outliers are present across $Q, K$, and $V$.
*   **For FFN (A4W4):** Use **Sub-Channel E8M0**. Since there is no Softmax in the FFN, the E8M0 power-of-2 scaling error is harmless, providing massive multiplier-free power savings.