# SpinQuant: FFN Outlier Rotation & Smoothing

## The Bottleneck (FFN Outliers)
While Attention KV cache outliers can be tamed, the Feed-Forward Network (specifically the `down_proj` input that takes the SwiGLU activation) suffers from massive, non-symmetric outliers. Naive 4-bit subchannel quantization causes catastrophic clipping, dropping FFN SQNR to single digits.

## The ICML/ICLR Solution (QuaRot / SpinQuant)
Recent literature (e.g., QuaRot, SpinQuant) proposes inserting learned or random orthogonal rotation matrices ($R$) before quantization. 
*   Because $R$ is orthogonal, $R \cdot R^T = I$. 
*   We rotate the activations ($X \cdot R$) to smear the outliers across all channels.
*   We rotate the weights ($W \cdot R$) to match.
*   The math holds: $(X \cdot R) \cdot (W \cdot R)^T = X \cdot R \cdot R^T \cdot W^T = X \cdot W^T$.

## Hardware Prototype Results (Qwen2.5-1.5B)
We verified this theory by prototyping a random orthogonal rotation matrix applied to the `down_proj` of Qwen 1.5B Layer 12.
*   **Naive A4W4 FFN:** 6.79 dB
*   **Rotated A4W4 (SpinQuant):** 7.57 dB
*   **Verdict:** Rotation mathematically successfully mitigates outliers, recovering ~0.8 dB SQNR. However, for a full edge tape-out, computing the dense $X \cdot R$ rotation introduces $O(H^2)$ overhead. To make this viable for NPU latency, we must combine this rotation with NF4 LUTs and replace the dense $R$ with Chained Householder reflections.
