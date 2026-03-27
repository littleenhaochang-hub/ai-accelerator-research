# AI Accelerator Research & Quant Lab

This repository contains ongoing research, hardware simulations, agentic AI benchmarks, and quantitative trading algorithms.

## Active Projects

### 1. MoE Pre-Fetching & Caching (`/moe_prefetching`)
Simulating SSD-to-DRAM caching for Mixture-of-Experts (MoE) models (e.g., Qwen1.5-MoE, Mixtral, DeepSeek-Coder-V2).
*   Proved LRU caching fails (hit rate <25%).
*   Modeled *Forced Locality* (Oracle-MoE concept), improving DRAM cache hit rates to >75% via temporal routing smoothing.

### 2. Edge Agentic Browsing Benchmarks (`/chrome_mcp_agent`)
Measuring LLM performance (TPS and Latency) for autonomous web browsing using OpenClaw's Chrome MCP.
*   **Edge vs Cloud:** Benchmarked Llama 3.2 3B, Qwen 2.5 7B, DeepSeek-Coder-V2 16B against Gemini 2.5 Flash.
*   **Context Penalty:** Identified the $O(N^2)$ prefill bottleneck when passing raw 32K+ token DOM snapshots to local models.
*   **Long-Context Tests:** Implemented Needle-In-A-Haystack testing for local MLX models.

### 3. Quantitative Trading (`/quant_trading`)
Machine Learning algorithms for the US stock market (AI & Semiconductors) and Taiwan Stock Exchange (台股).
*   **v1.0 Algorithm:** Random Forest classifier predicting daily price movements based on momentum (RSI, MACD) and volatility (Bollinger Bands). Backtested against historical data.

---
*Auto-managed by OpenClaw Assistant.*