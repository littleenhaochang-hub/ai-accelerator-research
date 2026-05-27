# Hardware Dynamic Layer Thresholding Engine (HW-DLTE)
## 針對大語言模型 FFN 冗餘深度的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
在大語言模型 (如 LLaMA) 中，高達 2/3 的計算量與參數集中在 Feed-Forward Network (FFN) 中。然而，研究指出對於許多相對簡單的 Token，網路底層特徵已足夠決定輸出，後續的 FFN 計算大多是冗餘的。但由於軟體調度缺乏彈性，系統仍強制所有 Token 走完深達數十層的 FFN。

### 2. 探索文獻 (Explore)
我們提出 Hardware Dynamic Layer Thresholding Engine (HW-DLTE)。在每一層 FFN 入口處設置一個硬體等級的信心評估器 (Confidence Evaluator)。硬體會快速計算 Token 區塊的早期信心分數，若閾值達標，排程器將瞬間繞過 (Bypass) 該層 FFN 的 MAC 運算陣列與權重讀取。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_dlte_sim.py` 進行 64K Context 模擬驗證：
- **Baseline FFN Latency:** 206163.43 ms
- **HW-DLTE Latency:** 92772.09 ms
- **Speedup (加速比):** 2.22x
- **MAC 計算與記憶體頻寬縮減:** 55.0%

### 4. 結論
實作 HW-DLTE 能夠帶來 2.22x 的計算加速，並直接省下 55% 的總算力與讀取功耗。建議將此「動態層級旁路引擎」整合入大語言模型專用的 Edge NPU 核心排程器中，以極大化能源效率。
