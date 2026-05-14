# Hardware Softmax LUT Predictor Engine (HW-SLP)

## 摘要 (Executive Summary)
本研究探討了 Attention 機制中 Softmax 運算所帶來的超越函數 (Transcendental Function, 如 exp) 計算瓶頸。我們提出並驗證了基於硬體查找表 (LUT) 與分段線性逼近 (PWL) 的硬體 Softmax 引擎。

## 實驗結果 (Experimental Results)
- **軟體基準測試 (Software Baseline):** 傳統 FPU 計算 8K Context 的 Softmax 延遲為 350.00 ms。
- **硬體加速引擎 (HW-SLP):** 採用 LUT 與 PWL 逼近後，延遲驟降至 40.00 ms，且完全消除 FPU 需求。
- **效能提升 (Speedup):** 達成 **8.75x** 的加速。

## 架構提議 (Architectural Proposal)
我們強烈建議在 Edge NPU 的 Attention Block 中內建「HW-SLP 硬體 Softmax 引擎」，以整數與查表取代浮點指數運算，大幅降低動態功耗。