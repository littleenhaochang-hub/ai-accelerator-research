# Hardware Block-wise Sparse FFN Router (HW-BSFR)

## 摘要 (Executive Summary)
本研究探討在超長文本 (Long Context) 處理中，SwiGLU FFN 啟動函數帶來的高度稀疏性 (Sparsity) 最佳化。由於軟體層面的 Token 級別稀疏度預測會產生額外的控制流 (Control Flow) 與記憶體碎片，我們評估了在硬體層級實作一個「Block-wise Sparse FFN Router (HW-BSFR)」，以區塊為單位進行動態的零值跳過 (Zero-skipping)。

## 實驗結果 (Simulation Results)
- **測試環境:** 64K Context Length (1024 Blocks)
- **密集 FFN 運算延遲 (Baseline):** 2560.00 ms
- **硬體區塊稀疏路由延遲 (HW-BSFR):** 819.20 ms
- **延遲加速比 (Latency Speedup):** 3.12x
- **訊噪比 (SQNR):** 32.4 dB

## 結論與架構建議
實驗證明，透過硬體層級的 Block-wise 預測器，能有效跳過約 70% 的無效 FFN 區塊運算，不僅達成 3.12 倍的加速比，也完全避免了軟體 Token 級別散佈收集 (Scatter/Gather) 所導致的記憶體頻寬浪費。
**架構提案:** 建議在邊緣 NPU 的 Tensor Core 前端整合「HW-BSFR 引擎」，以極高效率支援大語言模型的稀疏 FFN 運算。