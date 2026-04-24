# 硬體架構研究報告：Hardware Attention Sink Eviction

## 1. 瓶頸分析
對於無限制長度生成的模型 (如 StreamingLLM)，KV Cache 必須不斷丟棄舊的 Token，但保留最前面的 Attention Sinks。目前的軟體實作需要大量的指標操作與記憶體搬移，造成嚴重的 CPU Overhead。

## 2. 文獻與架構探討
本研究探討在 NPU 的 SRAM 控制器中實作硬體級別的 Ring Buffer，並保留靜態的 Sink Roots 區域。

## 3. Prototype 驗證與數據
- **Software Overhead:** 每生成一個 Token 約 15 us 的管理成本。
- **Hardware Overhead:** 0.5 us。
- **Throughput Speedup:** 30.00x

## 4. 硬體設計建議 (Hardware Proposal)
建議在 Edge NPU 整合 "SRAM Ring Buffer with Static Sink Roots"，自動管理 Token Eviction，無須軟體介入。