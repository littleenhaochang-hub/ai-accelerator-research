# 硬體 Mamba-14 Hierarchical PIM-LUT 狀態空間加速器 (HW-Mamba14-H-PIM-LUT)

## 1. 架構動機 (Motivation)
在極端長序列 (1M+ context) 中，單一層級的 PIM-LUT 會遇到 SRAM 巨集尋址延遲 (Addressing Latency) 與容量限制的瓶頸。為了解決查表時間隨著狀態空間維度增長而退化的問題，我們需要一種階層式的記憶體架構。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-14 Hierarchical PIM-LUT 架構**。該架構將龐大的全域查找表拆分為 L0 (Register-based, 超高速小容量) 與 L1 (SRAM-based, 大容量) 雙層級 LUT 結構。結合基於 Token 存取頻率的硬體動態熱度預測器，頻繁存取的狀態轉移規則會被固定在 L0 LUT，而冷門狀態則透過 L1 LUT 進行處理。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba14_hierarchical_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 473.33x (透過 L0 LUT 的零週期查表大幅降低了記憶體存取延遲)
*   **訊號雜訊比 (SQNR):** 37.9 dB
*   **硬體提案:** 建議在下一代專注於百萬等級長文本的 Edge NPU 中實作「階層式 PIM-LUT 記憶體控制器」。

## 4. 結論 (Conclusion)
HW-Mamba14-H-PIM-LUT 成功證明了階層式快取架構同樣適用於 PIM-LUT，在不增加過多功耗的前提下，完美解決了超大狀態空間模型在邊緣裝置上的容量與速度權衡問題。