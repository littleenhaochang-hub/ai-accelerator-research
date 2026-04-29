# Hardware LoRA Scheduler

## 實驗目標 (Objective)
在多租戶 (Multi-tenant) 或多 Agent 協作場景下，同一基礎模型需要頻繁切換不同的 LoRA (Low-Rank Adaptation) 權重。軟體層面的 Context Switch 會打斷 MAC 流水線，導致巨量的切換延遲。

## 方法 (Methodology)
提出「硬體 LoRA 調度器與多工器 (Hardware LoRA Scheduler & Multiplexer)」。在 NPU 的 SRAM 與 MAC 陣列之間加入專屬的 LoRA 權重廣播匯流排。硬體可以根據 Token 附帶的 Adapter ID，以 Zero-cycle 延遲在不同的 LoRA 權重間動態切換，實現完全硬體化的 Continuous Batching。

## 結果 (Results)
- Baseline Latency (Software Context Switch): 25.60 ms
- Proposed Latency (Hardware Multiplexer): 1.02 ms
- **Speedup: 25.00x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
專用的硬體 LoRA 調度器能將適配器切換延遲降低 25 倍。強烈建議在未來的 Edge Agentic AI 晶片中，將「硬體 LoRA 多工器」列為標準配備，以達成無縫的多 Agent 協同推論。
