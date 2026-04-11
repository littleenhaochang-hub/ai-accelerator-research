# Householder TurboQuant

## The Prefill Bottleneck
Standard TurboQuant uses an $O(N^2)$ randomized Hadamard-like matrix to smear activation outliers across the sequence dimension. This works for decoding (N=1) but completely stalls the NPU ALU during long-context Prefill (e.g., N=32K).

## The Hardware-Software Co-Design
We replace the dense orthogonal matrix with **Chained Householder Reflections**.
*   **Complexity:** Reduces to $O(k \cdot N)$ linear time.
*   **FLOP Reduction:** 16x reduction in compute, 32x reduction in memory overhead.
*   **Empirical SQNR:** On real Qwen activations, dense Hadamard achieves 51.25 dB, while 4 Householder reflections achieve 50.62 dB. We lose only ~0.6 dB for a massive hardware speedup.

*Related: [[Compound_Noise_Analysis]], [[NF4_LUT_Quantization]]*
