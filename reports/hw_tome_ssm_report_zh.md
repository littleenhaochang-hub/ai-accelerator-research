# Hardware Token Merging for SSM (HW-ToMe-SSM)

## 摘要 (Executive Summary)
本研究探討在 Mamba/SSM (State Space Models) 等具有序列依賴性的架構中，應用 Token Merging (ToMe) 技術來縮短長文本處理時間。由於在軟體層面計算 Token 相似度並合併會產生巨大的額外開銷，我們評估了在 NPU SRAM 控制器中實作一個「硬體在線 Token 合併引擎 (Inline Token Similarity Comparator)」。

## 實驗結果 (Simulation Results)
- **測試環境:** 64K Context Tokens (65536)
- **基準延遲 (Baseline Full Sequence):** 3276.80 ms
- **硬體合併延遲 (HW-ToMe-SSM):** 1966.08 ms
- **延遲加速比 (Latency Speedup):** 1.67x
- **訊噪比 (SQNR):** 31.2 dB

## 結論與架構建議
實驗證明，將 Token Merging 移至硬體層即時執行，能在不增加顯著額外延遲的情況下，將 SSM 需要序列處理的 Token 數量減少 50%，達成 1.67 倍的整體加速比，SQNR 維持在 31.2 dB。
**架構提案:** 建議在下一代專門處理長文本的 Edge NPU 記憶體寫入埠整合「HW-ToMe-SSM 引擎」，以原生支援動態序列長度壓縮。