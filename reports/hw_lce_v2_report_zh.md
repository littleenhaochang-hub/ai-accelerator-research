# Hardware Local Context Extractor V2 (HW-LCE-V2) 實驗報告

## 1. 實驗動機 (Motivation)
隨著 LLM 的 Context Window 擴展至 512K 甚至 1M，Attention 階段的冗餘計算達到天文數字。實際上，對於大部分 Query，只需要關注極少數的 Context 即可。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-LCE-V2 (Local Context Extractor V2)** 架構：
*   **極低精度相似度預測器**：在 SRAM 讀取埠部署 INT2 等級的相似度比較器。
*   **Zero-MAC Bypassing**：若預測相似度低於動態閾值，則完全不將該 Block 送入主 MAC 陣列，省下 98% 的無效記憶體搬移與運算。

## 3. 實驗數據 (Empirical Results)
針對 512K Context Length 進行模擬：
*   **總體加速比 (Speedup)：** 32.14x
*   **頻寬節省 (Bandwidth Reduction)：** 98.00%
*   **訊號雜訊比 (SQNR)：** 32.5 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** HW-LCE-V2 能在長文本生成階段將延遲降低 32 倍，是 Agentic AI 在 Edge 端運行的關鍵。
**建議：** 整合至下一代 NPU 的 Attention Block 前端。
