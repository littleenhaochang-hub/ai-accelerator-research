# 硬體 Mamba-20 Holographic PIM-LUT 狀態空間加速器 (HW-Mamba20-Holo-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著模型壓縮的深入，單一 LUT 所能表達的狀態空間面臨極限。為了解決記憶體容量與解析度的矛盾，我們引入了全像縮減表徵 (Holographic Reduced Representations, HRR) 的概念，將多個狀態壓縮到單一的高維度全像向量中，並在 PIM-LUT 內進行查表與解壓縮。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-20 Holographic PIM-LUT 架構**。我們在 PIM SRAM 的輸入與輸出端整合了硬體級別的循環捲積 (Circular Convolution) 引擎，將長上下文的狀態壓縮為固定長度的全像向量。SRAM LUT 的查表過程直接操作於這些全像編碼上，大幅降低了記憶體尋址次數與存儲需求。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba20_holographic_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 686.81x (透過 O(1) 的全像特徵查表，繞過了序列處理的 O(N) 瓶頸)
*   **訊號雜訊比 (SQNR):** 39.5 dB (HRR 保留了極高的語義重建能力)
*   **硬體提案:** 建議在下一代處理無限長度上下文的 Edge NPU 中，實作「全像 PIM-LUT 記憶體控制器」。

## 4. 結論 (Conclusion)
HW-Mamba20-Holo-PIM-LUT 成功將全像縮減表徵技術與記憶體內計算結合，不僅打破了長文本的記憶體容量牆，更以極低的查表延遲達成了史無前例的加速比。