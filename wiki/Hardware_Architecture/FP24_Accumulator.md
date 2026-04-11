# FP24 Accumulator

## Overview
In Dense Compute (MAC Arrays), the adder tree and accumulator registers consume significant chip area and power. We proved that reducing the global accumulator from FP32 to FP24 saves ~25% of the accumulator physical footprint.

## Functional Verification
We ran a full-model validation on `Qwen2.5-1.5B`, replacing all 196 linear layers with a vectorized chunk-based FP24 accumulator.
*   **Baseline (FP32):** WikiText-2 PPL = 6.650
*   **FP24 (Chunk=32, RNE Rounding):** WikiText-2 PPL = 6.651
*   **Conclusion:** Degradation (+0.001) is statistically indistinguishable.

## Critical Implementation Details
*   **Chunk Size:** Accumulation must occur in local INT32 chunks (e.g., 32 elements) before global FP24 reduction.
*   **Rounding Mode:** Simple truncation destroys SQNR (drops to 55dB). Hardware must implement Round-to-Nearest-Even (RNE) by adding half the dropped precision (`0x00000080` in FP32 int representation) before shifting. This rescues SQNR to 82dB.

*Related: [[Compound_Noise_Analysis]]*
