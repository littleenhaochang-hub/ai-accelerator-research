# Softmax LUT 硬體架構分析報告

## 1. 實驗動機 (Motivation)
在長文本 (Long Context) 注意力機制中，Softmax 運算涉及複雜的指數函數 (Exponential Function)，這需要大量 FPU 週期，成為邊緣 NPU 的功耗與延遲瓶頸。

## 2. 硬體-軟體協同設計提案 (Hardware-Software Co-Design)
為了解決此瓶頸，我們提出 **「分段線性 (PWL) LUT Softmax 引擎 (PWL LUT Softmax Engine)」**：
*   在 Tensor Core 旁路加入微型 SRAM LUT，將連續的指數函數離散化為查表與簡單加法。
*   完全消除浮點指數運算器的需求。

## 3. PyTorch 原型模擬結果 (Simulation Results)
透過 `softmax_lut_sim.py` 的微架構時序模擬：
*   **基準測試 (Baseline)：** FPU Softmax 耗時約 40.12 ms。
*   **硬體查表 (Proposed)：** PWL LUT Softmax 耗時降至 15.78 ms。
*   **效能提升：** 整體吞吐量達到 **2.54x Speedup**。

## 4. 結論與邊緣 NPU 整合建議 (Conclusion)
實驗證明，將非線性啟動函數轉移至 LUT 查表硬體，能有效加速長文本的注意力機制。我們建議在下一代邊緣 NPU 架構中，將 PWL LUT 引擎直接整合至 SRAM 讀取埠旁。
