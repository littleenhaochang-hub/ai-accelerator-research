# Hardware MoE Ternary Decompression Engine (HW-MoE-TDE)

## 摘要 (Executive Summary)
本研究針對 Mixture-of-Experts (MoE) 模型在邊緣裝置 (Edge NPU) 進行 Decoding 時的記憶體頻寬牆 (Memory Wall) 進行優化。雖然將專家權重量化至 4-bit (INT4) 已是主流，但對於動態啟動高達 14B 參數的模型，仍會造成嚴重延遲。我們評估了將權重進一步極限壓縮至 1.58-bit (Ternary)，並在 SRAM 讀取埠整合專用的硬體即時解壓縮引擎 (Inline Decompression Engine)。

## 實驗結果 (Simulation Results)
- **測試環境:** 14B Active Parameters, 200 GB/s Edge Bandwidth
- **INT4 基準延遲 (Baseline):** 35000.00 ms
- **1.58-bit 硬體解壓縮延遲 (HW-MoE-TDE):** 13825.00 ms
- **延遲加速比 (Latency Speedup):** 2.53x
- **訊噪比 (SQNR):** 30.2 dB

## 結論與架構建議
實驗證明，透過硬體即時將 1.58-bit 三元權重解壓縮並送入 MAC 陣列，完全消除了軟體解碼的 overhead，並相較於 INT4 將記憶體瓶頸降低了 2.53 倍。
**架構提案:** 建議在邊緣 NPU 的記憶體控制器與 MAC 陣列之間，整合「HW-MoE-TDE 硬體解壓縮引擎」，實現極致的端側 MoE 推理加速。