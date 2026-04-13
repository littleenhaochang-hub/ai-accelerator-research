# Extreme Sub-3-Bit Quantization (W2A4 & W2A2)

## The Allure of 2-Bit Limits
As Edge NPUs hit memory bandwidth walls, shrinking from 4-bit to 2-bit (e.g., Ternary `[-1, 0, 1]`, like BitNet 1.58b) offers a theoretical pathway to a 0.12x memory footprint. This would allow a massive 30B parameter model to run entirely out of a phone's 4GB RAM partition.

## Hardware Prototype Verdict (Qwen2.5-1.5B)
We ran a Subchannel (Block Size 128) Post-Training Quantization (PTQ) test specifically isolating the Feed-Forward Network (`down_proj`) to observe the signal collapse.

| Configuration | Memory Footprint | SQNR (dB) |
| :--- | :--- | :--- |
| **W4A4 (Subchannel B128)** | 0.25x | 11.91 dB |
| **W2A4 (Subchannel B128)** | 0.19x | **2.41 dB** |
| **W2A2 (Subchannel B128)** | 0.12x | **0.39 dB** |

## The "Death Line" Analysis
Our previous end-to-end ablation studies established that **3.40 dB SQNR is the "Death Line"** for the Qwen architecture. Below this threshold, the model outputs completely hallucinated, out-of-vocabulary (OOV) tokens.
*   **Zero-Shot (PTQ) 2-bit is Mathematically Dead:** Slicing the tensor into 128-element blocks and clamping the values to just `[-1, 0, 1]` instantly drops the SQNR to 2.41 dB (for W2A4) and 0.39 dB (for W2A2). The quantization noise completely overwhelms the neural signal.
*   **The Hardware Implications:** You cannot simply apply PTQ (Post-Training Quantization) or dynamic scaling to deploy an existing FP16 model in 2-bit on an Edge NPU. To unlock 2-bit (0.12x memory), the model **must** be trained from scratch natively in 2-bit (Quantization-Aware Training, QAT), forcing the gradients to structurally adapt to the ternary weight landscape.
