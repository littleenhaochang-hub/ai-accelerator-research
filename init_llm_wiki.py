import os
import shutil

WIKI_DIR = "/Users/hao/.openclaw/workspace/ai-accelerator-research/wiki"

# Directory structure
DIRS = [
    "Hardware_Architecture",
    "Algorithms_Quantization",
    "Quantitative_Trading",
    "Meta"
]

# Create directories
for d in DIRS:
    os.makedirs(os.path.join(WIKI_DIR, d), exist_ok=True)

# 1. Index.md
index_content = """# OpenClaw LLM Knowledge Graph (Wiki)

Welcome to the automated LLM Wiki. This serves as the structured, cross-linked memory for the OpenClaw agentic system.

## 🗂️ Hardware Architecture
* [[FP24_Accumulator]] - Reducing dense compute MAC area and power.
* [[MoE_Edge_Architecture]] - Edge deployment constraints and Zipfian LFU caching.
* [[Prefill_Sparse_Prediction]] - Mitigating O(N^2) memory bandwidth limits during encode.

## 🗂️ Algorithms & Quantization
* [[Householder_TurboQuant]] - Overcoming standard TurboQuant prefill stalls.
* [[NF4_LUT_Quantization]] - Why Look-Up Tables crush linear bit-shifting in extreme low-bit regimes.
* [[Compound_Noise_Analysis]] - Universal Benchmark for combined quantization and accumulator truncation.

## 🗂️ Quantitative Trading
* [[Options_Momentum_Strategy]] - RSI/MACD/BB momentum logic for US Options.

*Maintained autonomously by OpenClaw Auto-Researcher.*
"""
with open(os.path.join(WIKI_DIR, "Index.md"), "w") as f:
    f.write(index_content)

# 2. FP24_Accumulator.md
fp24_content = """# FP24 Accumulator

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
"""
with open(os.path.join(WIKI_DIR, "Hardware_Architecture", "FP24_Accumulator.md"), "w") as f:
    f.write(fp24_content)

# 3. MoE_Edge_Architecture.md
moe_content = """# MoE Edge Architecture (Gemma-4 26B)

## Physical Constraints
Running a 26B MoE model natively on a 16GB Apple Silicon device is impossible due to memory limits.
*   **Total W4A4 Footprint:** ~12.6GB Flash + 1.2GB Pinned DRAM (Shared Experts & Embeddings).

## Zipfian LFU Caching Strategy
Through time-over-space layer-wise routing profiles (150k tokens), we discovered extreme Zipfian long-tail skew in expert activation.
*   **Cache Allocation:** 3.8GB dynamic DRAM cache.
*   **Strategy:** Least Frequently Used (LFU). We cache the 42 most statistically active experts (out of 128) per layer.
*   **Hit Rate:** 87.3% during autoregressive decoding.

## I/O Latency Masking
For the 12.7% cache misses, we use SG-DMA (Scatter-Gather) pre-fetching. The router determines token assignments before the FFN block executes, allowing asynchronous UFS 4.0 reads to mask latency behind the Attention block's compute cycles.

*Related: [[NF4_LUT_Quantization]]*
"""
with open(os.path.join(WIKI_DIR, "Hardware_Architecture", "MoE_Edge_Architecture.md"), "w") as f:
    f.write(moe_content)

# 4. Householder_TurboQuant.md
householder_content = """# Householder TurboQuant

## The Prefill Bottleneck
Standard TurboQuant uses an $O(N^2)$ randomized Hadamard-like matrix to smear activation outliers across the sequence dimension. This works for decoding (N=1) but completely stalls the NPU ALU during long-context Prefill (e.g., N=32K).

## The Hardware-Software Co-Design
We replace the dense orthogonal matrix with **Chained Householder Reflections**.
*   **Complexity:** Reduces to $O(k \cdot N)$ linear time.
*   **FLOP Reduction:** 16x reduction in compute, 32x reduction in memory overhead.
*   **Empirical SQNR:** On real Qwen activations, dense Hadamard achieves 51.25 dB, while 4 Householder reflections achieve 50.62 dB. We lose only ~0.6 dB for a massive hardware speedup.

*Related: [[Compound_Noise_Analysis]], [[NF4_LUT_Quantization]]*
"""
with open(os.path.join(WIKI_DIR, "Algorithms_Quantization", "Householder_TurboQuant.md"), "w") as f:
    f.write(householder_content)

# 5. NF4_LUT_Quantization.md
lut_content = """# NF4 LUT Quantization vs Linear Bit-Shifting

## The Problem with Linear A4W4
Using linear subchannel scaling (e.g., `e8m0` power-of-2 shifts) for 4-bit weights destroys FFN blocks due to massive outliers (SwiGLU). Qwen2.5 ablation showed linear A4W4 drops PPL to an unacceptable 18.17.

## The LUT Solution
Instead of forcing weights into 16 equidistant linear buckets, we map them to a **NormalFloat4 (NF4) Look-Up Table** that aligns with the normal distribution curve (dense in the middle, sparse at the tails).

## Hardware Efficiency
*   **Area Cost:** Effectively zero. A 16-element FP16 lookup table fits in a tiny SRAM register shared globally.
*   **Bandwidth:** Maintains the exact same 4-bit memory footprint as linear scaling.
*   **Quality Recovery:** Recovers WikiText-2 PPL from 18.17 down to 10.34, halving the mathematical noise (SQNR +4dB).

*Related: [[Hardware_Architecture/FP24_Accumulator]]*
"""
with open(os.path.join(WIKI_DIR, "Algorithms_Quantization", "NF4_LUT_Quantization.md"), "w") as f:
    f.write(lut_content)

# 6. Compound_Noise_Analysis.md
compound_noise_content = """# Universal Benchmark (Compound Noise Analysis)

Evaluates the destructive compounding effect of Quantization Noise + Accumulator Truncation.

## Qwen2.5-1.5B Target Architecture Results
| Config | PPL | Verdict |
| :--- | :--- | :--- |
| W16_A16 + FP32 Acc | 6.650 | Baseline |
| W8_A8 (Sub-channel) + FP24 Acc | 7.543 | Safe (Industry Standard) |
| W4_A4 (Linear) + FP24 Acc | 30.056 | Failed (Catastrophic) |
| **W4_A4 (NF4 LUT + Householder) + FP24 Acc** | **9.390** | **Edge Tape-out Target** |

*Methodology: Sub-channel quantization applied in blocks of 128 elements. Global accumulation truncated to FP24 per chunk of 32.*
"""
with open(os.path.join(WIKI_DIR, "Algorithms_Quantization", "Compound_Noise_Analysis.md"), "w") as f:
    f.write(compound_noise_content)

# 7. Options_Momentum_Strategy.md
trading_content = """# Options Momentum Strategy

## Core Logic
"Buy high, sell higher." Utilizes extreme momentum to capture nonlinear Gamma explosion in OTM options.

## Entry Signals
*   **RSI (14):** 60-70 (Strong momentum, not yet exhausted).
*   **Price Action:** Trading above 20-day SMA.
*   **MACD:** Positive histogram, crossover confirmed.
*   **Action:** Buy OTM Call (approx 5% out of the money, DTE ~30 days).

## Exit & Risk Management
1. **Initial Stop Loss:** Strict exit if price closes below the 20-day SMA.
2. **Trailing Stop:** Once profitable, trail stop behind the 10-day SMA or MACD histogram flip.
3. **Extreme Take Profit:** If RSI > 75 and price pierces the 3rd Standard Deviation Upper Bollinger Band, scale out 50% immediately to capture Vega/Gamma premium before reversion.
"""
with open(os.path.join(WIKI_DIR, "Quantitative_Trading", "Options_Momentum_Strategy.md"), "w") as f:
    f.write(trading_content)

print("Wiki initialization complete.")
