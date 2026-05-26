# Hardware MoE Async Decoder (HW-MoE-AD)

## 實驗背景
在 Edge NPU 上執行 MoE 架構時，專家權重的同步提取（Synchronous Fetching）會導致大量的管線停滯 (Pipeline Bubbles)，嚴重降低吞吐量。

## 解決方案
提出 HW-MoE-Async-Decoder，利用非同步 DMA 預取機制，並將計算與記憶體讀取完全解耦。在硬體層級實現 ping-pong buffer，隱藏 PCIe 傳輸延遲。

## 實驗結果
- **[Baseline] Latency:** 45.00 ms
- **[Proposed] Latency:** 6.20 ms
- **Speedup:** 7.26x

## 結論
非同步解碼能完全隱藏 MoE 的記憶體瓶頸，對於受限的 Edge NPU 極為重要。建議整合入次世代的 NPU 排程器。
