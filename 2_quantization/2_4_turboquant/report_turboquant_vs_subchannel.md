# TurboQuant vs Sub-Channel Quantization: The Hardware Tradeoff

**Date:** March 31, 2026

When targeting W4A4 (4-bit Weights, 4-bit Activations), the primary obstacle is massive feature outliers in the activation tensors. There are two leading methods to mitigate this: **TurboQuant** (Orthogonal Rotation) and **Sub-Channel Quantization** (Grouped / Block Quantization).

We developed a PyTorch script (`exp_turboquant_vs_subchannel.py`) to directly compare their reconstruction Signal-to-Noise Ratio (SNR) and hardware overheads on a `[256, 4096]` LLM activation matrix with extreme injected outliers.

## 1. The Methodologies

*   **Sub-Channel Quantization (Group Size = 32):**
    Instead of calculating a single FP16 scale factor for the entire 4096-dim token vector, the vector is split into 128 distinct blocks of 32 elements. Each block calculates its own `max-abs` scale factor. If an extreme outlier (e.g., `30.0`) exists, it only ruins the 4-bit precision for its specific block of 32 elements. The other 127 blocks retain pristine precision.
*   **TurboQuant (Orthogonal Rotation):**
    The vector is multiplied by a dense, orthogonal matrix ($X \cdot R$) before quantization. The rotation mathematically smears the energy of the outlier evenly across all 4096 dimensions. A single FP16 scale factor is then used to quantize the entire "smoothed" 4096-dim token vector into 4-bit.

---

## 2. Experimental Results (Reconstruction SNR)

| Quantization Method | Reconstruction SNR (dB) | Mechanism |
| :--- | :--- | :--- |
| **Naive 4-Bit (Token-wise)** | 2.53 dB | *Fails catastrophically due to outliers.* |
| **TurboQuant (Rotation)** | 16.00 dB | *Smeared outliers protect the overall distribution.* |
| **Sub-Channel Quant (G=32)** | **18.58 dB** | *Outlier isolation yields higher absolute accuracy.* |

---

## 3. The True Hardware Tradeoff

While Sub-Channel Quantization slightly outperforms TurboQuant mathematically (+2.5 dB), the choice for Edge Accelerators (like Apple Silicon) comes down to **Compute Overhead vs. Memory Overhead**.

### A. The Memory Overhead Tax (Sub-Channel's Flaw)
To achieve that 18.58 dB, Sub-Channel Quantization requires 128 FP16 scale factors per token instead of 1.
For a sequence of 256 tokens:
*   **TurboQuant Scale Memory:** `512 Bytes`
*   **Sub-Channel Scale Memory:** `65,536 Bytes` (128x more memory!)
In a long-context scenario (32K+ tokens), managing, loading, and broadcasting hundreds of thousands of independent FP16 scale factors creates a secondary memory-bandwidth wall for the ALU.

### B. The Compute Overhead Tax (TurboQuant's Flaw)
TurboQuant keeps the scale memory footprint tiny (1 scale per token), but it introduces severe **computational overhead**. Before the vector can be quantized, it must be multiplied by a $4096 \times 4096$ orthogonal rotation matrix $R$. That is a massive $O(N^2)$ GEMM operation per token just to prepare the data for quantization.
*(Note: As proven in Pillar 4, replacing the dense random $R$ matrix with an $O(N \log N)$ Hadamard Transform or an $O(k \cdot N)$ Chained Householder Reflection significantly mitigates this compute penalty).*

## Verdict for Edge NPUs
*   **If your NPU is Memory-Bandwidth Constrained:** Use **TurboQuant (with Householder Reflections)**. It sacrifices a small amount of accuracy (16 dB vs 18 dB) and burns some extra ALUs, but keeps the KV Cache and Activation scale factor memory footprint virtually non-existent.
*   **If your NPU is Compute-Constrained (Weak ALUs, High SRAM):** Use **Sub-Channel Quantization**. It requires zero additional multiplications ($X \cdot R$) and isolates the outliers perfectly, provided the hardware can stream the 128x scale factors efficiently.