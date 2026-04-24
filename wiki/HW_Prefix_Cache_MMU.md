# Hardware Token MMU (硬體 Prefix Caching 記憶體管理單元)

## 實驗背景 (Background)
在多 Agent 並發或是多輪對話的情境中，Prefix Caching (前綴緩存) 能大幅減少重複 System Prompt 的 Prefill 計算量。然而，現有的軟體框架 (如 vLLM) 使用 Radix Tree 來進行前綴比對與虛擬記憶體映射，這會對 CPU 造成極大負擔，並且在調度 KV Cache 時引發延遲。

## 物理模擬 (Physical Simulation)
透過 `hw_prefix_cache_mmu_sim.py`，我們比較了 CPU 軟體 Radix Tree 與硬體 MMU Page Table Walker 的延遲：
- **軟體 Radix Tree 延遲 (1000 requests)**: 500.00 ms
- **硬體 MMU Page Table Walker 延遲**: 20.00 ms
- **整體加速比**: 25.00x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 的 SRAM 記憶體控制器中，加入 **「Hardware Token MMU」**。
其運作原理如同 CPU 的 TLB (Translation Lookaside Buffer)。當 NPU 需要讀取 KV Cache 時，直接將 Virtual Token Sequence ID 送入 MMU，硬體自動解析 Radix Tree 並返回 Physical SRAM Address。這實現了「零 CPU 介入」的多路徑共享記憶體 (Zero-Copy Prefix Caching)，對 Agentic AI 推理效率有決定性的提升。
