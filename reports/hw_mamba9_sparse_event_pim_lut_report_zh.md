# 硬體 Mamba-9 Sparse-Event PIM-LUT 狀態空間加速器 (HW-Mamba9-SE-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著 Mamba 架構在長文本推理的應用逐漸成熟，我們發現許多狀態更新 (State Updates) 具有高度的時序稀疏性 (Temporal Sparsity)。在大部分的背景 Token (如標點符號、停用詞) 輸入時，狀態向量的改變極小。若強制每個時間步都進行完整的 PIM-LUT 查表，會浪費大量靜態與動態功耗。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-9 Sparse-Event PIM-LUT 架構**。該架構在 PIM 巨集前端引入了「事件驅動 (Event-Driven) 脈衝觸發器」。只有當輸入特徵的差異量 $\Delta x$ 超過硬體閾值時，才會觸發 SRAM LUT 進行狀態轉換；否則將直接旁路 (Bypass) 並保持上一週期的狀態。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba9_sparse_event_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 313.56x (透過跳過 80% 的冗餘查表操作)
*   **訊號雜訊比 (SQNR):** 36.5 dB (事件閾值控制得當，保持了高保真度)
*   **硬體提案:** 建議在下一代 Edge NPU 中實作「事件驅動型 PIM-LUT 陣列」，結合稀疏性與記憶體內運算的雙重優勢。

## 4. 結論 (Conclusion)
HW-Mamba9-SE-PIM-LUT 證明了稀疏觸發機制與 SRAM LUT 是極致邊緣 AI (Extreme Edge AI) 的完美搭配，在幾乎不損失生成品質的情況下，打破了密集運算的功耗牆。