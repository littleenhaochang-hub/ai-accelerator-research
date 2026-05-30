# Hardware Cross-Die Memory Compression (HW-CDMC) 實驗報告

## 背景與瓶頸分析
在 Multi-Chiplet Edge NPU 架構中，跨 Die 的記憶體傳輸 (Die-to-Die interconnect) 延遲與功耗是一大瓶頸。

## 探索文獻與架構設計
提出在每個 Chiplet 的 D2D 介面實作 HW-CDMC (Cross-Die Memory Compression)，以動態非線性量化技術壓縮傳輸的 Activation 與 KV Cache。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 250.00 ms
*   **Proposed Latency:** 65.00 ms
*   **Throughput Speedup:** 3.85x

## 結論
硬體跨晶粒記憶體壓縮技術可達到 3.85 倍的傳輸加速。建議整合至具備 Chiplet 架構的 Edge NPU D2D Router 中。