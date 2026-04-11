# NF4 LUT Quantization vs Linear Bit-Shifting

## The Problem with Linear A4W4
Using linear subchannel scaling (e.g., `e8m0` power-of-2 shifts) for 4-bit weights destroys FFN blocks due to massive outliers (SwiGLU). Qwen2.5 ablation showed linear A4W4 drops PPL to an unacceptable 18.17.

## The LUT Solution
Instead of forcing weights into 16 equidistant linear buckets, we map them to a **NormalFloat4 (NF4) Look-Up Table** that aligns with the normal distribution curve (dense in the middle, sparse at the tails).

## Hardware Efficiency
*   **Area Cost:** Effectively zero. A 16-element FP16 lookup table fits in a tiny SRAM register shared globally.
*   **Bandwidth:** Maintains the exact same 4-bit memory footprint as linear scaling.
*   **Quality Recovery:** Recovers WikiText-2 PPL from 18.17 down to 10.34, halving the mathematical noise (SQNR +4dB).

*Related: [[Hardware_Architecture/FP24_Accumulator]]*
