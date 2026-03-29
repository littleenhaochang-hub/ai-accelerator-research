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

## Active Projects

### 1. W4A4 FFN Quantization (`/w4a4_quantization`)
*   Modeled the catastrophic failure of naive 4-bit uniform quantization caused by extreme activation outliers.
*   **AGOR Architecture:** Prototyped *Adaptive Group-wise Outlier Retention*, slashing memory footprint by 5.4x (5.93 bits/val) while restoring Cosine Similarity to 97.69%.

### 2. KV Cache Compression (`/turboquant`)
*   Simulated Google's ICLR 2026 **TurboQuant** algorithm (Random Rotation + 1-bit QJL Residuals), verifying a 4x memory reduction at >90% accuracy.
*   **Auto-Research Breakthrough:** Replaced the $O(N^2)$ dense random rotation matrix with a hardware-friendly *Randomized Butterfly Transform*. Reduced memory footprint by 96% and sped up the transform 2.21x while maintaining 91.07% accuracy.

### 3. MoE Pre-Fetching & Caching (`/moe_prefetching`)
*   Simulated SSD-to-DRAM caching for Mixture-of-Experts (MoE) models (e.g., Qwen1.5-MoE, Mixtral).
*   Proved naive LRU caching fails (hit rate <25%).
*   Modeled *Forced Locality*, improving DRAM cache hit rates to >75% via temporal routing smoothing.

### 4. Edge Agentic Browsing Benchmarks (`/chrome_mcp_agent`)
*   Measuring LLM performance (TPS and Latency) for autonomous web browsing using OpenClaw's Chrome MCP.
*   Benchmarked Llama 3.2 3B, Qwen 2.5 7B, DeepSeek-Coder-V2 16B against Gemini 2.5 Flash, identifying the $O(N^2)$ prefill bottleneck when passing raw 32K+ token DOM snapshots to local models.

---
*Auto-managed by OpenClaw Assistant.*