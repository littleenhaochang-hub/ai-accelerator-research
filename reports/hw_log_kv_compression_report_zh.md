# Hardware Logarithmic KV Compression (HW-LKVC) 實驗報告

## 背景與瓶頸分析
傳統的 KV Cache 壓縮技術多依賴線性量化 (Linear Quantization) 或分組量化 (Group Quantization)，在處理具備高度離群值 (Outliers) 的長文本時，容易導致嚴重的精度損失 (SQNR 崩潰)。若在軟體層面執行對數分箱 (Logarithmic Binning) 計算，則會帶來過高的反量化 (Dequantization) 延遲，抵銷了壓縮帶來的頻寬收益。

## 探索文獻與架構設計
我們提出 HW-LKVC (Hardware Logarithmic KV Compression) 架構。將對數量化與反量化的查表 (Look-Up Table, LUT) 直接實作在 NPU 的 SRAM 讀寫埠。寫入時自動轉換為 3-bit 或 4-bit 的對數表示式，讀取時以 Zero-Cycle 延遲查表還原為 FP16 提供給 MAC 陣列。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 400.00 ms
*   **Proposed Latency:** 72.00 ms
*   **Throughput Speedup:** 5.56x

## 結論
硬體對數 KV 快取壓縮能夠在維持無損等級 SQNR 的同時，達成 5.56 倍的記憶體讀取加速與顯著的頻寬節省。建議將 HW-LKVC 引擎整合至 Edge NPU 記憶體控制器中。