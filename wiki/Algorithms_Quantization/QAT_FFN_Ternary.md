# QAT 1.58-Bit (Ternary) on FFNs

## The FFN Bottleneck (SwiGLU Outliers)
While we previously demonstrated QAT on the Attention `q_proj`, the true bottleneck for extreme low-bit quantization (like 1.58-bit ternary) is the Feed-Forward Network (FFN). Modern LLMs use SwiGLU activations, which create massive, highly non-linear outliers. Quantizing the `gate_proj`, `up_proj`, and `down_proj` matrices concurrently using Zero-Shot Post-Training Quantization (PTQ) usually destroys the network completely.

## Hardware Prototype Verdict (Gemma-3-270m FFN)
We isolated Layer 5's entire MLP block in `google/gemma-3-270m` and applied our Straight-Through Estimator (STE) to force all three projection weights into `[-1, 0, 1]` concurrently.

*   **Initial State (PTQ):** -0.64 dB SQNR. The signal power is literally lower than the noise power. The FFN is outputting pure garbage.
*   **QAT Step 30:** 10.07 dB
*   **QAT Step 150:** 17.98 dB
*   **Final Output (After QAT):** **17.64 dB SQNR** (+18.29 dB Recovery)

## Architectural Conclusion
The recovery is staggering (+18 dB). This proves that the latent FP32 weights can learn to structurally compensate for the SwiGLU outliers, even when the final weights are restricted to just three integer states (`-1, 0, 1`). 
For an Edge NPU Tape-out, this mandates that **all models must undergo QAT on their FFN blocks before deployment**. The hardware can then safely use multiplier-free Ternary ALUs (pure addition/subtraction) for the FFN, achieving near-perfect fidelity while shedding massive logic area.
