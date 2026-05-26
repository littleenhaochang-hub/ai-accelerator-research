# Hardware PEFT State Caching (HW-PSC) 實驗報告

## 摘要 (Executive Summary)
在 Mixture-of-Agents 或多租戶邊緣設備 (Multi-tenant Edge AI) 情境下，系統需要頻繁在多個 LoRA/PEFT 模型間切換。軟體層級的權重置換 (Swapping) 會產生巨大的 DRAM 到 SRAM 複製延遲。本實驗評估將多個 LoRA Adapter 快取於專用 SRAM，並透過硬體多工器 (Multiplexer) 進行零週期切換。

## 實驗結果
- **Software PEFT Switching Latency**: ~5.50 ms
- **HW-PSC Latency**: ~0.05 ms
- **Speedup**: 107.96x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 NPU 內建「硬體 PEFT 狀態快取 (HW-PSC)」與基底指標多工器 (Base-pointer Multiplexer)，可以消除上下文切換的記憶體搬移開銷。我們建議在 Edge NPU 記憶體控制器中實作此架構，以原生支援多 Agent 協同工作。
