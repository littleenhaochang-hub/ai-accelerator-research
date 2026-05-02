# Hardware LoRA Context Switcher 模擬報告

## 摘要 (Executive Summary)
本報告探討在 Multi-Agent 並行推論系統中，將 LoRA (Low-Rank Adaptation) 權重的動態切換從 CPU/PCIe (軟體控制) 轉移至 NPU 內建的 SRAM Bank 切換機制 (硬體多工器)。

## 實驗設計 (Experimental Design)
- 模擬 128 個 Agent 輪詢發出推論請求時的權重切換延遲。
- 軟體延遲基於標準 PCIe 頻寬與 CPU 驅動程式開銷；硬體延遲基於 SRAM 記憶體分頁的多工器硬體選擇 (Hardware MUX)。

## 實驗結果 (Results)
- **SW Latency**: 6.4000 s
- **HW Latency**: 0.1280 s
- **Speedup**: 50.00x

## 架構建議 (Architectural Proposal)
導入「Hardware LoRA Context Switcher (HLCS)」能將 Agent 任務切換的整體延遲減少 50 倍。強烈建議在下一代 Agentic Edge NPU 中，保留 10-20MB 的專用 LoRA SRAM Banks 並搭配硬體層級的 Base-Pointer 切換器，以達成極低延遲的多重人格/多工作代理並發推論，完全解除 PCIe 頻寬瓶頸。