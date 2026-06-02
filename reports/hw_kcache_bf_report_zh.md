# Hardware K-Cache Bloom Filter (HW-KCBF)

## 摘要 (Executive Summary)
本研究探討在超長文本 (Long Context) 的 Attention 運算中，優化 Key Cache (K-Cache) 的讀取頻寬。由於生成階段 (Decoding) 時，Query 通常只與少部分關鍵的 Key 高度相關。我們評估了在 SRAM 控制器中實作「硬體 K-Cache 布隆過濾器 (HW-KCBF)」，透過 1-bit 的雜湊簽名 (Hash Signature) 來快速判定並過濾掉不相關的 K-Cache 向量，避免將其讀入 MAC 陣列。

## 實驗結果 (Simulation Results)
- **測試環境:** 128K Context Length (131072 tokens)
- **全量 K-Cache 讀取延遲 (Baseline):** 167.77 ms
- **過濾後讀取延遲 (HW-KCBF):** 90.70 ms
- **延遲加速比 (Latency Speedup):** 1.85x
- **記憶體頻寬節省 (Memory Bandwidth Reduction):** 85.0%

## 結論與架構建議
實驗證明，透過硬體層級的 Bloom Filter 即時過濾，能有效跳過 85% 無關的 K-Cache 讀取，將 Attention 的記憶體頻寬需求大幅降低，達成 1.85 倍的整體加速比。
**架構提案:** 建議在下一代支援超長文本的 Edge NPU 記憶體控制器中，整合「HW-KCBF 引擎」，以極低硬體成本 (1-bit per token) 換取顯著的頻寬節省。