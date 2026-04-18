# 🤖 AI Accelerator Research Pillars & Empirical Findings
**Date:** 2026-04-18
**Architect:** Ghost

This report summarizes the empirical findings, mathematical bottlenecks, and next steps across our 8 active Hardware-Software Co-Design research pillars.

## 🧱 Pillar 1: Model Architecture
* **1.2 SSM / Mamba Hybrids:** 
  * **Empirical Finding:** At 4K context, standard $O(N^2)$ GEMM attention outpaces naive $O(N)$ sequential RNN scans on Apple Silicon (MPS). The Arithmetic Intensity of Mamba is only ~0.0002 (extreme memory-bound).
  * **Solution Prototype:** `block_parallel_scan.py` breaks the $O(N)$ sequential dependency, mimicking $O(\log N)$ Triton thread-block execution.
* **1.3 Linear Sliding Window:**
  * **Empirical Finding:** Implemented an $O(N)$ sliding window attention block tailored for 32K DOM parsing. Exported PyTorch graph into pure `sliding_window.tflite` via Google `litert-torch`.

## 🧱 Pillar 2: Quantization
* **2.6 AdaHOP: Adaptive Hadamard Rotation:**
  * **Empirical Finding [✅ SUCCESS]:** Simulated dynamic selection of Hadamard rotation axes (Row-wise, Column-wise, None) based on outlier shapes. Naive W4A4 achieved 19.16 dB SQNR. AdaHOP achieved 29.65 dB SQNR (+10.49 dB).
  * **Architectural Action:** Integrates directly into Block 32 Micro-Scaling to eliminate INT4 precision collapse.
* **2.2 1.58-Bit Ternary MACs (BitNet):**
  * **Empirical Finding [❌ BOTTLENECK]:** Quantizing to `[-1, 0, 1]` drops MAC power by replacing multipliers with adders, but Post-Training Quantization (PTQ) accuracy drops to ~5.8 dB SNR. Rescaling back to FP16 causes severe pipeline stalls on rigid NPUs.

## 🧱 Pillar 3: Dynamic Execution
* **3.1 Token-Level Early-Exit Routing:**
  * **Empirical Finding:** Forcing 80% of "easy" tokens to skip the last 8 layers reduces theoretical FLOPs/Latency by ~38%.
  * **Hardware Death-Knell:** The memory bandwidth overhead of PyTorch `gather/scatter` (boolean masking) for sparse token routing is slower than computing the full dense matrix. Needs dedicated sparse hardware logic.

## 🧱 Pillar 4: Memory-Centric (KV Cache & Attention)
* **4.3 FlashMLA-ETAP (Efficient Transpose Attention):**
  * **Empirical Finding [⏳ PENDING]:** DeepSeek's MLA compresses KV capacity but causes massive Compute-bound SRAM congestion during the Decode Up-projection phase.
  * **Hardware Solution:** Designing a "Hardware Transpose SRAM Buffer" to align the KV context length with the $M$-dimension of Tensor Cores (WGMMA) before MAC execution.

## 🧱 Pillar 5: On-Device Learning
* **5.1 Edge QLoRA Architecture:**
  * **Empirical Finding [❌ BOTTLENECK]:** While QLoRA compresses trainable parameters to < 0.4%, the Forward Activation Memory Wall is catastrophic. PyTorch must store the full 4K context activation tensor $X$ (>16GB SRAM) for backprop, forcing OS SSD swapping. Requires Transpose-Free Backprop algorithms.

## 🧱 Pillar 7: Dynamic Hardware Reconfiguration
* **7.1 PD-Swap (Dynamic Partial Reconfiguration):**
  * **Empirical Finding [⏳ PENDING]:** Evaluates reconfiguring the Matrix Engine between Prefill (compute-heavy) and Decode (memory-heavy) phases. Theoretical claims of 1.3x - 2.1x decode speedup without area increase.

## 🧱 Pillar 8: Quantization-Aware Training (QAT)
* **8.1 2-Bit (Ternary) QAT Architecture:**
  * **Empirical Finding:** Post-Training Quantization (PTQ) completely fails below 3.40 dB SQNR (the Qwen Death Line) for W2A4.
  * **Action Plan:** Abandon PTQ for extreme low-bit. Shift entirely to Quantization-Aware Training (QAT) using Straight-Through Estimators (STE) during backprop to force the network to adapt to the `[-1, 0, 1]` landscape.
