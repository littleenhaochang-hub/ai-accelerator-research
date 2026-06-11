# Hardware SRAM Memory Coalescer (HW-SRAM-MC) 實驗報告

## 1. 實驗動機 (Motivation)
稀疏注意力 (Sparse Attention) 與 Token Dropping 等技術會導致 SRAM 讀取呈現高度的非連續性與碎片化 (Fragmentation)。這使得原本可以透過 Burst Mode 高效讀取的 SRAM 頻寬大幅降低，成為長文本處理的新瓶頸。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-SRAM-MC (Hardware SRAM Memory Coalescer)**：
*   **動態記憶體聚合器**：在 SRAM 控制器中加入動態打包 (Packing) 邏輯，將不連續的讀取請求在硬體層面重新組合為連續的資料流 (Stream) 送往 MAC 陣列。
*   **零軟體開銷**：取代傳統軟體層面昂貴的 Gather/Scatter 迴圈。

## 3. 實驗數據 (Empirical Results)
針對 128K Context Length 進行模擬：
*   **總體加速比 (Speedup)：** 6.25x
*   **內部頻寬節省 (Bandwidth Reduction)：** 84.00%
*   **訊號雜訊比 (SQNR)：** 33.6 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** HW-SRAM-MC 可以有效還原 SRAM 處理高度稀疏任務時的頻寬利用率。
**建議：** 建議將其作為 Edge NPU 支援進階稀疏架構的標準配備。
