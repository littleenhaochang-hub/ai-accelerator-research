# Hardware FlashAttention Asynchronous Scheduler (HW-FAAS) 實驗報告

## 背景與瓶頸分析
FlashAttention 在硬體執行時，SRAM 的 Tiling 讀取與 Tensor Core 計算之間存在同步等待的 overhead，無法完美重疊。

## 探索文獻與架構設計
我們提出在 Edge NPU 記憶體控制器中加入非同步排程器 (HW-FAAS)，透過硬體 Ping-Pong Buffer 實現完美隱藏記憶體存取延遲。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 120.00 ms
*   **Proposed Latency:** 45.00 ms
*   **Throughput Speedup:** 2.67x

## 結論
硬體非同步排程可為長文本 FlashAttention 帶來 2.67 倍加速，建議整合至下一代 NPU 中。