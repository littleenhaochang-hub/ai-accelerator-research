# Strategies for SNR Recovery in Fused 4-Bit Attention

**Date:** March 30, 2026
**Context:** Following the discovery of the "Softmax Cliff" when fusing 4-bit Activations (A4) with TurboQuant KV caches, we must deploy variance mitigation techniques to recover the lost Signal-to-Noise Ratio (SNR).

## 1. 1-Bit Residual Correction (QJL) - The TurboQuant Method
Instead of accepting the noisy dot product $\hat{Q} \cdot \hat{K}^T$, we calculate the residual error during compression: $E_k = K - \hat{K}$ and $E_q = Q - \hat{Q}$. We compress this error down to a single bit (just the sign: +1 or -1). During inference, we perform the dense 4-bit MACs, then add back the 1-bit residual dot product. It acts as an unbiased statistical estimator that pushes the logit back toward its true FP32 value right before the Softmax amplification.
- **Pros:** True to the original TurboQuant paper, statistically robust.
- **Cons:** Requires a secondary 1-bit MAC operation (which is extremely fast on modern NPUs via popcount).

## 2. Variance-Aware Temperature Scaling
Quantization noise acts exactly like increasing the "temperature" of the LLM—it flattens the attention distribution. Because we can mathematically model the variance of 4-bit uniform noise ($\sigma^2$), we can dynamically scale the logits by a factor of $\sqrt{1 + \sigma^2_{noise}}$ *before* the Softmax. This artificially "cools" the logits, restoring the sharpness of the attention peaks and preventing the noise from shifting the probability mass to incorrect tokens.
- **Pros:** Zero memory overhead, $O(1)$ compute overhead.
- **Cons:** Only a statistical scalar fix; doesn't correct individual token errors.

## 3. Sparse Outlier Retention (Hybrid FP16/Int4)
Leveraging the Adaptive Group-wise Outlier Retention (AGOR) from Pillar 2.1. Instead of forcing the rotation matrix to smear *everything*, we extract the top 0.1% most extreme outliers and leave them in FP16. We rotate and 4-bit quantize the remaining 99.9%. The matrix engine executes the dense 4-bit math, and a tiny sparse FP16 kernel adds the outlier spikes back in. This almost entirely eliminates the cross-term variance ($e_q \cdot e_k$) that causes the catastrophic dB drop.
- **Pros:** Highest possible absolute accuracy retention.
- **Cons:** Sparse memory gather operations and branching are notoriously slow and hostile to Edge NPUs / Apple Silicon neural engines.

---

## Architectural Selection: 1-Bit Residual Correction (QJL)

I have selected the **1-Bit Residual Correction** as the superior architecture for our Edge AI accelerator roadmap. 

**Rationale:**
1. While Sparse FP16 (Option 3) is highly accurate, branching and sparse memory accesses completely destroy the latency benefits on Apple Silicon and edge NPUs. 
2. Temperature scaling (Option 2) is computationally free but mathematically weak for localized, high-magnitude token errors. 
3. The 1-Bit Residual (Option 1) perfectly balances the need for hardware-friendly dense execution (since 1-bit math reduces to ultra-fast bitwise XNOR/Popcount) while providing rigorous mathematical recovery of the attention logits right before they hit the Softmax cliff.

We will proceed with implementing the 1-Bit Residual prototype to measure the exact dB recovery.