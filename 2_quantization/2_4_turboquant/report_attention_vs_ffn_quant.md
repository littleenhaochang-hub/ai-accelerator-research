# Dual-Layer Evaluation: Attention vs FFN Activation Quantization

**Date:** March 31, 2026

We updated our architectural evaluation standard. Moving forward, all activation quantization algorithms must be tested against both the **Attention** input tensor and the **FFN Post-SiLU** input tensor. 

The rationale is that FFN activations behave fundamentally differently than Attention inputs: they are expanded to massive dimensions (e.g., 11008 in LLaMA), passed through asymmetric non-linearities (SiLU/GeLU), and contain extreme, structural channel-wise outliers (e.g., `> 150.0`).

We ran our 4-way quantization suite (`exp_attention_vs_ffn_quant.py`) to determine if **Sub-Channel E8M0** holds up against **TurboQuant** under the immense skew of the FFN layer.

---

## 1. Experimental Results (Math SNR)

### A. Attention Activations (Mostly Gaussian, Mild Outliers)
| Quantization Method | Reconstruction SNR (dB) |
| :--- | :--- |
| Naive 4-Bit | `4.69 dB` |
| TurboQuant (Rotation) | `16.05 dB` |
| Sub-Channel (E8M0, G=32) | **`16.16 dB`** |
| Sub-Channel (FP16, G=32) | `19.29 dB` |

### B. FFN Post-SiLU Activations (Asymmetric, Massive Structural Outliers)
| Quantization Method | Reconstruction SNR (dB) |
| :--- | :--- |
| Naive 4-Bit | `5.14 dB` |
| TurboQuant (Rotation) | `15.70 dB` |
| Sub-Channel (E8M0, G=32) | **`18.35 dB`** |
| Sub-Channel (FP16, G=32) | `20.93 dB` |

---

## 2. Architectural Analysis

The empirical data reveals a massive architectural distinction between Attention and FFNs.

### Why TurboQuant Struggles with FFNs (15.70 dB)
TurboQuant assumes that multiplying the input by a random rotation matrix will yield a perfect zero-mean Gaussian distribution. However, FFN activations passed through SiLU are heavily asymmetric (almost entirely positive) with massive, rigid structural outliers. Rotating an asymmetric distribution does not perfectly center it at zero, causing the symmetric 4-bit bins `[-8, 7]` to be utilized inefficiently.

### Why Sub-Channel E8M0 Dominates FFNs (18.35 dB)
Sub-channel quantization perfectly isolates the massive SiLU structural spikes into their own 32-element blocks. Even when forced into a pure power-of-2 `E8M0` format, it significantly outperforms TurboQuant on the FFN layer (+2.65 dB).

### The Missing Memory Tax (The Deciding Factor)
In our previous analysis, we stated that Sub-channel quantization creates a massive "Memory Bandwidth Tax" by generating 128 scale factors per token, which breaks the NPU. 
**This is only true for the KV Cache (Attention).** 
In the KV cache, those 128 scale factors per token must be saved to SRAM/DRAM and retrieved during every generation step, destroying bandwidth. 
**In the FFN layer, there is no cache.** The FFN activations are computed dynamically, passed into the linear layer, and immediately discarded. The NPU can generate the 128 `E8M0` scales, pipe them directly into the local Block-Floating Point (BFP) registers, execute the multiplier-free matrix math, and flush them. 

---

## 3. Final Edge AI Architectural Blueprint (Updated)

Based on the dual-layer evaluation, the ultimate hybrid strategy for Edge NPUs (Multiplier-Free + Minimal Bandwidth) is:

1.  **KV Cache (Attention):** Use **TurboQuant + 1-Bit QJL**. You cannot afford the memory tax of storing 128 scales per token for 32K tokens. You must use the rotation matrix to squeeze the entire token into a single scale factor.
2.  **FFN Activations:** Use **Sub-Channel E8M0**. Since FFN scales are instantly discarded, the memory tax is irrelevant. E8M0 provides massively superior accuracy (18.35 dB) for the skewed SiLU outputs while completely eliminating FP16 hardware multipliers from the ALU.