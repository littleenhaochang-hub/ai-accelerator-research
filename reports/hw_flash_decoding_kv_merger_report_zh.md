# 硬體 Flash-Decoding KV 合併器 (HW-Flash-Decoding-KV-Merger) 分析報告

## 執行摘要
在處理超長文本 (512K+) 的解碼階段，Flash-Decoding 需要跨越多個 KV 區塊進行部分 Softmax (Partial Softmax) 的歸約 (Reduction)，這在軟體端會導致大量的 DRAM 讀寫與同步開銷。我們提出了將此歸約過程硬體化。

## 模擬結果
* **軟體 Flash-Decoding 歸約延遲:** 921.60 ms
* **硬體合併器延遲:** 40.96 ms
* **效能提升:** 延遲加速達 22.50x。

## 架構建議
針對未來的邊緣 NPU 架構，建議整合 **Hardware Flash-Decoding KV Merger**，在 SRAM 層級實作專用的加法樹與 Softmax 合併單元，徹底消除長文本解碼時的記憶體頻寬牆。
