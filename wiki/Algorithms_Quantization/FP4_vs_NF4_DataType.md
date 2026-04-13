# Subchannel FP4 (E2M1) vs NF4 vs INT4

## The Data Type War in 4-bit Quantization
When quantizing activations and weights in blocks (e.g., Subchannel Block Size = 128), selecting the right 4-bit format is as critical as the quantization algorithm itself.
*   **INT4 (Linear):** Distributes 16 values equally. Fails catastrophically on long-tail distributions.
*   **NF4 (NormalFloat4):** Look-Up Table strictly mapped to the cumulative distribution function (CDF) of a zero-mean Normal distribution.
*   **FP4 (OCP E2M1):** The new industry standard by the Open Compute Project. Uses 1 Sign bit, 2 Exponent bits, and 1 Mantissa bit. Unlike NF4, it has exact zeros and symmetric exponent clusters.

## Hardware Prototype Results
We ran a comparative grid directly on the `Qwen2.5-1.5B` FFN `down_proj` layer (W4A4) using a block size of 128.

| Data Type (Subchannel B128) | SQNR (dB) |
| :--- | :--- |
| **INT4 Linear (Uniform)** | 11.93 dB |
| **NF4 (NormalFloat4)** | 15.24 dB |
| **FP4 E2M1 (OCP Standard)** | **16.43 dB** |

## Architectural Verdict
While NF4 (15.24 dB) completely crushes naive INT4 (11.93 dB) by aligning with the bell curve, **FP4 E2M1 (16.43 dB)** proved to be the absolute winner for LLM FFN layers.
*   **Why FP4 wins:** The SwiGLU activation outputs are not a perfect Gaussian bell curve; they are heavily clustered near zero but with sudden, extreme positive outliers. The FP4 (E2M1) format intrinsically possesses dynamic range via its 2 exponent bits, allowing it to capture the near-zero sparsity perfectly while pushing the maximum representable value high enough to absorb the outliers without clipping.
*   **Tape-out Implication:** Moving away from NF4 LUTs to native **FP4 (E2M1) MAC units** (or emulating them via LUT) is the optimal path for maximizing FFN fidelity.
