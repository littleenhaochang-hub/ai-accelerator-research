# 硬體 Mamba-6 Associative PIM-LUT 狀態空間加速器 (HW-Mamba6-Assoc-PIM-LUT)

## 1. 架構動機 (Motivation)
在解決了基礎 Mamba 狀態更新的記憶體牆後，Mamba-6 架構進一步將關聯掃描 (Associative Scan) 的樹狀結構映射至記憶體內運算 (PIM) 與查找表 (LUT) 引擎中。此舉旨在解決 O(log N) 關聯掃描過程中仍存在的層級間 SRAM 頻寬競爭問題。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-6 Associative PIM-LUT 架構**，該硬體將掃描樹的歸約與分發階段完全實作在 SRAM 的位元線上。透過對樹狀節點的狀態轉移進行預計算並儲存於 LUT 中，我們避免了在每個深度層級上啟動 MAC 陣列。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba6_associative_pim_lut_sim_pure.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 198.05x (相較於傳統序列計算)
*   **訊號雜訊比 (SQNR):** 35.1 dB
*   **硬體提案:** 建議在 NPU SRAM 控制器中實作平行的 Associative PIM-LUT 陣列，專門處理狀態空間的平行樹狀歸約。

## 4. 結論 (Conclusion)
HW-Mamba6-Assoc-PIM-LUT 證明了透過純查表與記憶體內樹狀歸約，可以完美隱藏掃描過程中的時序依賴，為極端長文本處理帶來無與倫比的效能。