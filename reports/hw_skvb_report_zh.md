# Hardware Sparse KV Bypasser (HW-SKVB)

## 摘要 (Executive Summary)
本研究針對超長文本 (Long Context) 在 Decoding 階段的 KV Cache 記憶體頻寬牆進行優化。在生成階段，模型通常只會強烈關注極少數的 Token (如 Attention Sinks 或關鍵字)。我們評估了在記憶體控制器中整合一個基於低精度的「硬體 KV 旁路器 (HW-SKVB)」，用於預測並動態跳過不重要的 KV Cache 讀取。

## 實驗結果 (Simulation Results)
- **測試環境:** 128K Context Length (131072 tokens)
- **密集解碼延遲 (Baseline):** 10485.76 ms
- **硬體稀疏讀取延遲 (HW-SKVB):** 2228.22 ms
- **延遲加速比 (Latency Speedup):** 4.71x
- **訊噪比 (SQNR):** 32.1 dB

## 結論與架構建議
實驗證明，透過硬體即時預測並過濾 80% 的冗餘 KV Cache 讀取，可將 128K 長文本的 Decoding 延遲降低 4.71 倍，且不需軟體介入。
**架構提案:** 建議在邊緣設備 NPU 的 SRAM 控制器中整合「HW-SKVB 預測器」，以原生支援極低功耗的超長文本生成。