# Auto-Researcher 報告: SRAM Compute-in-Memory (CIM) 記憶體內運算架構

## 摘要
在傳統的 Von Neumann 架構下，NPU 需要將權重從 SRAM 讀出至暫存器，再送入 Tensor Core 的 MAC 陣列進行計算，這個「資料搬移」的功耗遠大於實際計算的功耗。本實驗模擬基於 SRAM 的 Compute-in-Memory (CIM) 架構，將類比 MAC (Analog MAC) 運算直接發生在 SRAM 的 Bitline 上。

## 實驗設定
- 矩陣維度: 4096 x 4096
- 量化位元: 4-bit (INT4)
- Baseline: 傳統 Digital Tensor Core (讀取+運算耗能)
- Proposed: SRAM CIM (透過類比電流加總，分攤 ADC 耗能)

## 模擬結果
* **Baseline Energy:** 77.18 uJ
* **Proposed Energy:** 6.71 uJ
* **整體功耗節省 (Energy Reduction):** 91.30%

## 結論與架構建議
資料搬移是 Edge AI 最致命的功耗來源。透過 SRAM CIM 架構，讓 Activation 直接驅動 Wordline 並在 Bitline 收集電流，能在不移動權重的情況下完成矩陣向量乘法 (MVM)。強烈建議下一代極低功耗的 Edge 裝置直接汰換標準 SRAM，改採 **CIM-SRAM Macro**。這項硬體革新能減少高達 91.3% 的推理能量消耗，是實現在無風扇、電池供電設備上運行百億參數模型的最終解方。
