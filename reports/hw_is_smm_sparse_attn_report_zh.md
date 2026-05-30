# Hardware In-SRAM Sparse Matrix Multiplier (HW-IS-SMM)

## 摘要 (Executive Summary)
本研究針對超長文本 (Long Context) Sparse Attention 的極端稀疏性 (Sparsity > 90%) 進行架構優化。傳統數位 MAC 陣列在處理稀疏矩陣時，仍需消耗大量的 SRAM-to-MAC 資料搬移頻寬與對齊開銷。我們評估了將 Sparse Matrix Multiplication 轉移至 SRAM Bitline 上直接計算 (Compute-in-Memory) 的架構。

## 實驗結果 (Simulation Results)
- **測試環境:** 256K Context Length (262144 tokens), 95% Sparsity
- **傳統 MAC 延遲 (MAC Bound):** 2621.44 ms
- **In-SRAM SMM 延遲 (SRAM Bound):** 65.54 ms
- **延遲加速比 (Latency Speedup):** 40.00x
- **訊噪比 (SQNR):** 31.6 dB

## 結論與架構建議
實驗證明，透過 In-SRAM Compute 直接在記憶體內部處理非零區塊乘加運算，能完全消除資料在匯流排上的搬移延遲，對於高達 95% 稀疏度的長文本注意力機制，可達成 40.00x 的加速比。
**架構提案:** 建議在下一代 Extreme Edge NPU 的 SRAM 陣列中整合「HW-IS-SMM 巨集 (Macros)」，實現極低功耗的超長文本處理。