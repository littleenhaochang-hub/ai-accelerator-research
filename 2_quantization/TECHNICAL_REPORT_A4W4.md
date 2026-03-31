# Technical Report: Edge AI Quantization Architectures for Sub-4-Bit LLM Inference

**Date:** March 31, 2026  
**Subject:** W4A4 and KV4 Architectures for Edge NPUs  

## Abstract
This report details the architectural evaluation of 4-bit activation and 4-bit weight (W4A4/KV4) quantization for Large Language Models (LLMs) on Edge Neural Processing Units (NPUs). We analyze the mathematical impact of activation outliers, the variance compounding effect in the Attention Softmax, and propose a dual-path hardware blueprint: Orthogonal Rotation (TurboQuant) + 1-Bit Residuals for Attention, and Sub-Channel E8M0 quantization for Feed-Forward Networks (FFNs).

---

## 1. Evaluation Metrics (The Dual-Validation Pipeline)

Evaluating sub-4-bit quantization solely on perplexity or post-softmax errors hides hardware-level bottlenecks. We established a dual-validation pipeline to measure both pure mathematical fidelity and live generative coherence.

### 1.1 Mathematical Fidelity: Signal-to-Noise Ratio (SNR)
We measure the exact matrix-engine error using the Signal-to-Noise Ratio (SNR), expressed in decibels (dB).
$$ \text{SNR (dB)} = 10 \cdot \log_{10}\left( \frac{\text{Var}(X_{true})}{\text{Var}(X_{true} - X_{quant})} \right) $$
*   **Logarithmic Scale:** A drop of 3 dB indicates that the variance of the quantization noise has exactly doubled.
*   **Empirical Thresholds:** 
    *   `< 10 dB`: Catastrophic failure. The model loses semantic grounding (outputs silence or repeating tokens).
    *   `14~15 dB`: Borderline. The model forms coherent syntax but suffers from severe hallucinations.
    *   `> 18 dB`: Safe zone. The quantization noise is suppressed enough to preserve the LLM's autoregressive logic.

### 1.2 Generative Coherence: Live Model Evaluation
To test the "Softmax Cliff" (where the exponential function non-linearly amplifies the quantization noise $e_q \cdot e_k$), we monkey-patch the quantization algorithms directly into a live `Qwen2.5-0.5B-Instruct` model. 
*   **Methodology:** The model runs a deterministic 10-prompt suite (covering math, coding, and reasoning). 
*   **Metric:** We measure the **Pass Rate (%)** of semantic coherence and factual accuracy, proving if the algorithm survives the chaotic autoregressive decoding loop.

---

## 2. Background & Quantization Algorithms

We evaluated four primary quantization algorithms to compress the activation matrix $X \in \mathbb{R}^{B \times S \times D}$.

### 2.1 Naive Uniform Quantization (Token-wise)
A single FP16 scale factor $s$ is calculated per token. 
$$ s = \frac{\max(|X|)}{2^{b-1} - 1} $$
$$ X_q = \text{round}\left(\frac{X}{s}\right) \cdot s $$
*   **Flaw:** LLM activations contain extreme structural outliers (e.g., magnitude > 100.0). These outliers stretch the scale $s$, compressing 99% of normal features into zero.

### 2.2 Sub-Channel Quantization (Grouped)
The token vector is divided into $G$ contiguous blocks (e.g., Group Size = 32). A distinct scale factor is calculated for each block $i$.
$$ X_{q, i} = \text{round}\left(\frac{X_i}{s_i}\right) \cdot s_i $$
*   **E8M0 Microscaling:** To eliminate the need for floating-point multipliers in the ALU, the scale $s_i$ can be forced to a power-of-2 (E8M0 format):
    $$ s_{e8m0, i} = 2^{\lceil \log_2(s_i) \rceil} $$
    This allows hardware dequantization using simple integer bit-shifts (`<< E`).

### 2.3 Orthogonal Rotation (TurboQuant)
Instead of isolating outliers, we spread their energy. The activation $X$ is multiplied by an orthogonal matrix $R$ (where $R \cdot R^T = I$).
$$ X_{rot} = X \cdot R $$
$$ X_q = \text{Quantize}(X_{rot}) $$
*   **Symmetry in Attention:** To maintain mathematical invariance in $Q \cdot K^T$, both the Query and the Key must be rotated by the same matrix $R$:
    $$ Q_{rot} \cdot K_{rot}^T = (Q R) \cdot (K R)^T = Q (R R^T) K^T = Q K^T $$

### 2.4 1-Bit QJL Residual Correction
To rescue the SNR from the "Softmax Cliff", we calculate the quantization error $E$, compress it to its sign (1-bit), and apply a mean scalar $\alpha$.
$$ E = X_{rot} - X_q $$
$$ R_{1bit} = \text{sign}(E) \cdot \frac{1}{D}\sum |E| $$
During inference, the dot product uses dense 4-bit MACs, plus a highly efficient bitwise `Popcount/XNOR` pass for the 1-bit residual.

---

## 3. Experimental Results

### 3.1 Attention Ablation (KV4 vs A4KV4)
We isolated the Attention block to measure the "Compounding Penalty" when shifting from FP32 queries (KV4) to 4-bit queries (A4KV4).

| Algorithm | Stage 1: KV4 SNR | Stage 2: A4KV4 SNR | $\Delta$ Penalty | Live Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Naive 4-Bit** | `7.70 dB` | `7.43 dB` | -0.27 dB | 0% |
| **Sub-Channel (E8M0)** | `8.22 dB` | `8.63 dB` | +0.41 dB | 0% |
| **Sub-Channel (FP16)** | `14.41 dB` | `14.18 dB` | -0.23 dB | 0% (Hallucinates) |
| **TurboQuant + 1-Bit QJL**| **`20.61 dB`** | **`18.69 dB`** | -1.92 dB | **40-60%** |

*   **Analysis:** Quantizing $Q$ introduces error $e_q$ that compounds with $e_k$. The exponential Softmax function amplifies this noise heavily. Sub-channel (E8M0) fails completely here (`8.63 dB`) because the power-of-2 scaling error shifts the Softmax probability mass to the wrong tokens. TurboQuant + 1-Bit QJL is the only survivor.

### 3.2 FFN vs Attention (The SiLU Skew)
We tested the algorithms on the FFN post-SiLU activations, which contain extreme asymmetric, structural outliers.

| Algorithm | FFN Post-SiLU SNR | Attention SNR |
| :--- | :--- | :--- |
| **TurboQuant (Rotation)** | `15.70 dB` | `16.05 dB` |
| **Sub-Channel (E8M0, G=32)** | **`18.35 dB`** | `16.16 dB` |

*   **Analysis:** TurboQuant assumes $X \cdot R$ creates a zero-mean Gaussian. However, SiLU activations are strictly non-negative. Rotating them fails to center them, wasting the negative bins of the `[-8, 7]` INT4 grid. Conversely, Sub-Channel E8M0 perfectly isolates the FFN structural outliers into 32-element blocks, achieving superior precision (`18.35 dB`).

---

## 4. Architectural Blueprint

Based on the dual-validation methodology, Edge NPUs require a bifurcated quantization architecture:

1.  **For KV Cache & Attention:** **TurboQuant + 1-Bit QJL**. 
    Sub-channel approaches generate 128 scale factors per token, requiring massive memory bandwidth for 32K contexts. TurboQuant uses $O(N^2)$ compute to smear outliers, reducing the scale to 1-per-token. The 1-bit residual perfectly rescues the Softmax distribution.
2.  **For FFN Activations:** **Sub-Channel E8M0 (Group=32)**. 
    FFN activations are discarded immediately after computation; there is no memory bandwidth tax for storing scales. E8M0 natively eliminates FP16 floating-point multipliers in the ALU, relying entirely on integer bit-shifts, while yielding superior SNR (`18.35 dB`) against asymmetric SiLU outliers.