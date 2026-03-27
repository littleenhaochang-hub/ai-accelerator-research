# GitHub Web Agent Benchmark: Token & Latency Report

This report details the token breakdown, throughput (TPS), and latency for the 4-turn GitHub repository analysis benchmark.

**Models Tested:**
- **Cloud:** Gemini-2.5-Flash (Processing full raw DOM)
- **Edge:** DeepSeek-Coder-V2:16b (Processing 16K truncated DOM on Mac mini)

## 1. Turn-by-Turn Token Stats

| Turn | Task | Model | Input Tokens | Output Tokens | Turn Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Identify first repo link | Gemini Flash | 4,497 | 130 | 23.9s |
| | | DeepSeek 16B | 4,547 | 128 | 24.4s |
| **2** | Extract Stars and Forks | Gemini Flash | 15,402 | 17 | 2.8s |
| | | DeepSeek 16B | 5,509 | 112 | 15.9s |
| **3** | Find 'Issues' tab link | Gemini Flash | 15,405 | 106 | 9.9s |
| | | DeepSeek 16B | 5,511 | 118 | 16.1s |
| **4** | Extract top open issue | Gemini Flash | 13,123 | 21 | 2.5s |
| | | DeepSeek 16B | 5,338 | 47 | 13.3s |

## 2. Throughput Summary (Tokens Per Second)

| Model | Input TPS (Prefill) | Output TPS (Generation) | Notes |
| :--- | :--- | :--- | :--- |
| **DeepSeek-Coder-V2 (16B)** | ~460 TPS | ~30 TPS | Consistent performance on Mac mini unified memory. |
| **Gemini-2.5-Flash** | Up to ~5,400 TPS | Near Instant | Massive context window natively handled. First-turn latency reflects cold start/network routing. |
