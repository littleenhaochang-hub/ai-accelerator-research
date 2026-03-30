# 1.58-Bit Ternary MAC (BitNet) Baseline & Bottleneck Analysis

**Date:** March 30, 2026
**Context:** Exploring extreme weight quantization ({-1, 0, 1}) to eliminate floating-point multiplications from Edge LLMs (Pillar 2.2).

## 1. The Algorithm
BitNet b1.58 quantizes all linear layer weights into a ternary format: `{-1, 0, 1}`. 
This means the dot product `Y = X * W^T` no longer requires Fused-Multiply-Add (FMA) units. Instead, it becomes pure additions and subtractions.

## 2. Experimental Results
An initial simulation (`exp_ternary_mac_baseline.py`) measured the mathematical accuracy (SNR) of this transformation on a typical `[128, 4096] x [4096, 4096]` LLM linear layer with injected outliers.

*   **FP32 Act $\times$ 1.58-Bit W:** `5.79 dB`
*   **8-Bit Act $\times$ 1.58-Bit W:** `5.78 dB`

## 3. The Bottlenecks (For Auto-Researcher to Improve)

This approach poses three severe challenges that the next wave of research must solve:

1.  **Catastrophic Math SNR (`~5.8 dB`):** 
    Compressing 16-bit Gaussian weights down to just three states `{-1, 0, 1}` destroys the variance of the weight matrix. The output logits suffer massive degradation. Without specialized pre-training (training the model from scratch to *expect* ternary weights), applying Post-Training Quantization (PTQ) to an existing model is mathematically fatal.
2.  **The Mixed-Precision Accumulator Stall:**
    While the integer math is fast, you still have to multiply the output by the scale factors ($\gamma_{weights} \times scale_{activations}$) in FP16 to get the final answer. Modern NPUs (like the Apple Neural Engine) are highly pipelined for uniform data types. Forcing them to accumulate in INT32, then cast to FP16, then multiply by a scalar, breaks the pipeline and introduces latency stalls that kill the theoretical speedup.
3.  **Outlier Sensitivity in Activations:**
    The script uses ABSMAX for the 8-bit activations. Because LLMs have massive outliers, the 8-bit grid is stretched, ruining the precision of the `X` matrix before it even hits the ternary `W`. 

## Next Steps for Auto-Researcher
*   **Fix 1:** Design an algorithm that absorbs the FP16 scale factors *into the activation function* (e.g., SiLU/GeLU) so the accumulator doesn't stall.
*   **Fix 2:** Try hybrid quantization—keeping 1% of the weights (the largest magnitudes) in FP16, and the remaining 99% in 1.58-bit, to recover the SNR.