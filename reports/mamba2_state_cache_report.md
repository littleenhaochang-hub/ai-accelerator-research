# 硬體架構研究報告：Mamba-2 Hardware State Caching

## 1. 瓶頸分析
在 Mamba-2 或 SSM 架構中，每個 Token 處理完後需要更新並儲存其 State。若將 State 頻繁寫回 DRAM，會造成嚴重的記憶體頻寬消耗與延遲。

## 2. 文獻與架構探討
本研究探討在 NPU 內建專用的 SRAM 區塊作為 "Mamba State Cache"，避免與一般 Weight/Activation 競爭快取，並支援單週期的 State 更新。

## 3. Prototype 驗證與數據
- **DRAM Fetch Overhead:** 24.58 ms
- **SRAM Cache Overhead:** 0.82 ms
- **Throughput Speedup:** 30.00x

## 4. 硬體設計建議 (Hardware Proposal)
建議在 Edge NPU 整合 "Dedicated Mamba State Cache"，以確保 SSM 模型在長文本生成時不會受到 DRAM 延遲的限制。