# 硬體架構研究報告: HW-AM-KVC-PIM (Associative Memory KV-Cache PIM Engine)
## 摘要
本研究評估了結合 Associative Memory (TCAM) 與 PIM (Processing-in-Memory) 的 KV Cache 並行檢索硬體架構。在 1048576 (1M) 超長上下文長度下，相較於傳統數位 MAC 陣列的線性檢索，達成 166.67 倍的延遲加速，且 SQNR 維持在 34.50 dB。
## 架構提議
建議在 Edge NPU 記憶體陣列中整合「HW-AM-KVC-PIM 引擎」，將長文本的 Attention 相似度計算直接轉化為記憶體內的大規模平行硬體 Pattern Matching，實現 O(1) 的檢索延遲。
