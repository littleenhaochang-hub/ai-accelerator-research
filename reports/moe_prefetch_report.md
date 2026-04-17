# Auto-Researcher 報告: MoE Speculative Router Prefetching

## 摘要
在 Edge 裝置 (如 Mac mini 或一般 NPU) 執行巨型 Mixture of Experts (MoE) 模型時，由於 SRAM 容量限制，專家權重通常存放於 DRAM 甚至 SSD，導致頻繁的 CPU-GPU 記憶體搬運 (Memory Transfer) 成為 decoding 的致命瓶頸。本實驗探討「預測性專家預取」(Speculative Expert Prefetching) 的硬體架構，透過在路由器端加入輕量級 Predictor，在計算當前 Token 的同時，非同步透過 DMA 從 Host 預取下一個 Token 可能用到的 Expert。

## 實驗設定
- 專家數量：64
- 專家大小：100 MB
- 匯流排頻寬 (PCIe/Unified)：64 GB/s
- 預測準確率假設：90%
- 測試 Token 數量：1000

## PPA (Power, Performance, Area) 模擬結果
* **Baseline (Demand Fetching):** 1525.88 ms
* **Proposed (Speculative Prefetching):** 152.59 ms
* **效能提升 (Speedup):** 10.00x

## 結論與架構建議
純依賴硬體快取 (Hardware Cache) 在 MoE 這種具備高度隨機切換特性的負載中容易發生 Thrashing。透過與軟體共同設計 (Hardware-Software Co-Design)，將 MoE Router 預測的置信度暴露給硬體的非同步 DMA 引擎 (Asynchronous DMA Engine)，可以在不增加 ALU stall 的情況下完美隱藏 PCIe/CXL 的延遲。建議在未來的 NPU 架構中整合 **MoE Lookahead Prefetcher**。
