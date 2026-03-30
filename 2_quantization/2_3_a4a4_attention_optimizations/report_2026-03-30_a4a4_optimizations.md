# Evaluation of A4A4 Attention Optimizations

**Date:** March 30, 2026
**Context:** Pushing 4-bit Activation $\times$ 4-bit Activation (A4A4) through the Dual-Validation pipeline to see if we can rescue generative quality without needing the TurboQuant orthogonal rotation or QJL residuals.

We evaluated three industry-standard techniques against a strict 4-bit baseline:
1. **Dynamic Percentile Clipping (p=0.99):** Clamping extreme outliers before quantization to preserve the dynamic range of the remaining 99%.
2. **Fine-Grained Block Quantization (Group Size = 32):** Quantizing the vector in chunks of 32 to isolate outlier distortion.
3. **Sparse-Dense Hybrid (SpQR Style):** Extracting the top 1% of outliers in pristine FP16, and only quantizing the remaining 99% to INT4.

---

## Gate A: Mathematical Validation (SNR in dB)

| Quantization Method | Phase 1: Pre-Softmax SNR | Phase 2: Post-Softmax SNR |
| :--- | :--- | :--- |
| **Naive A4A4** | 24.58 dB | 6.94 dB |
| **Percentile Clipping (p=0.99)** | 0.98 dB | -0.14 dB |
| **Block/Group Quant (G=32)** | 33.10 dB | 13.37 dB |
| **Sparse-Dense Hybrid (p=0.99)** | **41.23 dB** | **22.18 dB** |

*Analysis:* Percentile clipping failed catastrophically (0.98 dB) because those extreme LLM outliers are actually *critical* to the attention mechanism's logic. If you clip them, the math breaks. The Sparse-Dense hybrid scored an incredibly high 41.23 dB, proving that isolating the outliers mathematically solves the variance compounding problem.

---

## Gate B: Model-Level Evaluation (Qwen2.5-0.5B-Instruct)

Despite the mathematical success of Sparse-Dense and Grouped quantization, the live Generative Pass Rate revealed the brutal reality of the Softmax Cliff.

*   **FP16 Baseline:** Perfect coherence. ("The capital of France is Paris.")
*   **Naive A4A4:** Total collapse / silence.
*   **Percentile Clipping:** Outputted random tokens and corrupted text encoding (e.g., "A企业提供 I ampe C e B...").
*   **Block/Group Quant (G=32):** Recovered English grammar but hallucinated aggressively (e.g., *"The capital of France was Paris, which had been founded in 1657890912."*).
*   **Sparse-Dense Hybrid:** Failed to construct coherent sentences despite the high SNR (e.g., *"The provided by looking up to a description"*).

## Conclusion
The Dual-Validation methodology proved its worth. Even though the Sparse-Dense hybrid achieved a massive **41.23 dB** on the raw matrix math, it still failed the live text generation test. Why? Because extracting outliers into a sparse matrix and injecting them back dynamically interferes with complex structural mechanisms like Rotary Position Embeddings (RoPE) and shifts the Softmax mass just enough to confuse a fragile 0.5B model.

**Final Verdict:** None of these three A4A4 optimizations outperformed our **TurboQuant + 1-Bit QJL** residual approach. The rotation matrix + QJL residual remains the most robust solution for achieving Edge LLM coherence.