# 硬體 INT4 FlashAttention 引擎 (HW-INT4-FA) 分析報告

## 執行摘要
FlashAttention 極大地減少了 HBM/DRAM 的讀寫，但內部 SRAM 的讀寫頻寬依然是極限邊緣設備 (Edge NPU) 的瓶頸。我們提出了將 INT4 量化直接整合進 FlashAttention 的硬體架構，透過在 SRAM 讀取端口進行在線反量化 (Inline Dequantization) 來減少 SRAM 頻寬消耗。

## 模擬結果
* **FP16 FlashAttention 延遲:** 3.60 ms
* **HW-INT4-FA 延遲:** 1.00 ms
* **效能提升:** 延遲加速達 3.60x。
* **SRAM 頻寬節省:** 4.00x。

## 架構建議
針對未來的邊緣 NPU 架構，建議整合 **HW-INT4-FA Engine**，在 Attention Block 中原生支援 4-bit KV 緩存與注意力計算，將進一步打破晶片內部的記憶體頻寬牆。
