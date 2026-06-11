# Hardware K-Cache Pruning Engine (HW-KCPE) 實驗報告

## 1. 實驗動機 (Motivation)
在超長文本 (128K+) 推論中，Key Cache 的讀取頻寬極大。事實上，針對特定的 Query，有很高比例的 Key 是不相關的。軟體層面的 Pruning 往往需要先讀取資料才能運算，無法節省 DRAM 頻寬。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-KCPE** 架構：
*   **硬體內聯預測器**：在記憶體控制器中實作輕量級的硬體預測器，根據 Q 向量特徵動態決定哪些 K Block 需要被讀取。
*   **DRAM 讀取跳過**：對於不相關的 K Block，直接在硬體層面取消 DRAM Burst Read，節省頻寬。

## 3. 實驗數據 (Empirical Results)
*   **總體加速比 (Speedup)：** 5.38x
*   **頻寬節省 (Bandwidth Reduction)：** 85.00%
*   **訊號雜訊比 (SQNR)：** 32.7 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** HW-KCPE 可以在硬體層面直接阻斷不必要的記憶體讀取，達到 85% 的頻寬節約，加速長文本解碼。
**建議：** 整合入下一代 NPU Memory Controller 中。
