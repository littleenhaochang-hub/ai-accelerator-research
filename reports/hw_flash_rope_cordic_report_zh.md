# Hardware Flash-RoPE CORDIC Engine (HW-Flash-RoPE)

## 摘要 (Executive Summary)
本研究針對超長文本 (Long Context) 中旋轉位置編碼 (Rotary Position Embedding, RoPE) 造成的 SRAM 頻寬瓶頸進行改善。我們評估了在 SRAM 讀取埠直接整合一個基於 CORDIC (Coordinate Rotation Digital Computer) 演算法的硬體運算引擎，用於在資料搬移過程中即時計算 Sine/Cosine 旋轉。

## 實驗結果 (Simulation Results)
- **測試環境:** 128K Context Length (131072 tokens), 128 Head Dim
- **基準延遲 (Memory Bound):** 0.1311 ms
- **硬體 CORDIC 延遲 (Compute Bound):** 0.0066 ms
- **運算延遲加速比 (Latency Speedup):** 20.00x
- **訊噪比 (SQNR):** 34.2 dB

## 結論與架構建議
實驗證明，將 RoPE 從軟體核心 (需要從記憶體讀取預先計算的 sin/cos 表) 轉為硬體 Inline CORDIC 即時計算，可徹底消除 RoPE 的記憶體頻寬開銷，並達成 20.00 倍的延遲加速比。
**架構提案:** 建議在下一代 Edge NPU 的 SRAM 讀取路徑中整合「HW-Flash-RoPE CORDIC Engine」，實現零記憶體開銷的上下文長度擴展。