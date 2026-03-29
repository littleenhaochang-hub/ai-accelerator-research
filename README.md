# AI Accelerator Research & Quant Lab

This repository functions as a fully automated AI Scientist laboratory. It contains ongoing research, hardware simulations, agentic AI benchmarks, and PyTorch prototypes.

## 🎯 Core Research Directives

The `auto_researcher` engine driving this repository is explicitly focused on pushing the frontier of Artificial Intelligence hardware execution. It operates under two primary research pillars:

1. **Algorithm & Model Architecture Optimization (The Software Co-Design)**
   - Exploring sub-4-bit quantization (e.g., W4A4, W2A2), extreme KV Cache compression (TurboQuant), and Mixture-of-Expert (MoE) routing enhancements.
   - Prototyping novel Attention and Feed-Forward Network (FFN) architectures for Large Language Models (LLMs) and Image/Video Transformers.
2. **Hardware Architecture PPA Improvements (The Physical Silicon)**
   - Simulating and proposing physical hardware architectural improvements to maximize **PPA** (Power, Performance, Area).
   - Targeting Edge/Mobile NPU memory hierarchies, SSD-to-SRAM I/O bottlenecks, and Tensor Core utilization.

---

## 🏆 The Lab's Official Architectural Blueprint for Edge AI (2025/2026)

Based on empirical testing of extreme quantization techniques on Attention and FFN layers, we formally recommend the following unified **W3A4 / KV3+1** architecture for next-generation Edge NPUs (e.g., Apple Silicon M5/M6) and custom AI accelerators:

1.  **Model Weights (FFN & Attention): W3 (3-bit)**
    *   *Algorithm:* **AQLM** (Additive Quantization for LLMs).
    *   *Rationale:* Weights are static and easily compressed. Pushing weights to 3-bit maximizes memory bandwidth and allows massive models (10B+ parameters) to fit entirely within unified memory or high-speed SRAM.
2.  **Activations (FFN & Attention): A4 (4-bit INT)**
    *   *Algorithm:* **FlatQuant** (Channel-wise Affine Smoothing).
    *   *Rationale:* Activation outliers destroy naive INT4 quantization. We reject sparse branching techniques (like AGOR) because they bottleneck modern ALUs. Instead, applying channel-wise affine transformations mathematically squashes outliers *before* quantization, allowing Tensor Cores to execute pure, uninterrupted INT4 matrix math at >97% accuracy.
3.  **KV Cache (Memory Bandwidth Bottleneck): 3-bit Base + 1-bit Residual (4-bit Total)**
    *   *Algorithm:* **TurboQuant** paired with our custom **Chained Householder Reflections**.
    *   *Rationale:* Standard TurboQuant uses $O(N^2)$ random orthogonal matrices to smear outliers, which is fine for token-by-token Decode but catastrophically slows down long-context Encode (Prefill). Our lab proved that replacing this with $O(k \cdot N)$ Chained Householder Reflections reduces compute FLOPs by 16x and matrix memory by 32x, preserving >99% quantization fidelity while entirely eliminating the Prefill bottleneck.

---

## Active Projects

### 1. W4A4 FFN Quantization (`/w4a4_quantization`)
*   Modeled the catastrophic failure of naive 4-bit uniform quantization caused by extreme activation outliers.
*   **AGOR Architecture:** Prototyped *Adaptive Group-wise Outlier Retention*, slashing memory footprint by 5.4x (5.93 bits/val) while restoring Cosine Similarity to 97.69%.
*   **FlatQuant Affine Smoothing:** Simulated channel-wise min-max scaling to perfectly normalize outlier ranges into INT4 buckets without sparse branching.

### 2. KV Cache Compression (`/turboquant`)
*   Simulated Google's ICLR 2026 **TurboQuant** algorithm (Random Rotation + 1-bit QJL Residuals), verifying a 4x memory reduction at >90% accuracy.
*   **Auto-Research Breakthrough:** Replaced the $O(N^2)$ dense random rotation matrix with highly efficient *Chained Householder Reflections*. Slashed the matrix memory footprint by 32x and cut compute FLOPs by 16x, eliminating the Encode-phase bottleneck while maintaining 99.95% compression accuracy.

### 3. DeepSeek Multi-Head Latent Attention (`/deepseek_mla`)
*   Benchmarked DeepSeek's MLA architecture, proving an 8x reduction in KV Cache memory (32MB to 4MB for a 4K context slice).
*   **Fused Low-Rank Up-Projection:** Addressed the massive ALU compute penalty incurred when expanding the latent vector (`c_kv`) back into full K and V matrices during inference.

### 4. MoE Pre-Fetching & Caching (`/moe_prefetching`)
*   Simulated SSD-to-DRAM caching for Mixture-of-Experts (MoE) models (e.g., Qwen1.5-MoE, Mixtral).
*   Proved naive LRU caching fails (hit rate <25%).
*   Modeled *Forced Locality*, improving DRAM cache hit rates to >75% via temporal routing smoothing.

### 5. Edge Agentic Browsing Benchmarks (`/chrome_mcp_agent`)
*   Measuring LLM performance (TPS and Latency) for autonomous web browsing using OpenClaw's Chrome MCP.
*   Benchmarked Llama 3.2 3B, Qwen 2.5 7B, DeepSeek-Coder-V2 16B against Gemini 2.5 Flash, identifying the $O(N^2)$ prefill bottleneck when passing raw 32K+ token DOM snapshots to local models.