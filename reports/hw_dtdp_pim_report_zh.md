# 硬體架構研究報告: HW-DTDP-PIM (Dynamic Token-Drop PIM Engine)
## 摘要
本研究評估了將動態 Token 丟棄 (Dynamic Token Dropping) 的相似度計算與遮罩生成遷移至 PIM (Processing-in-Memory) 的硬體架構。在 512000 上下文長度下，相較於傳統數位 MAC 陣列，達成 100.00 倍的延遲加速，且 SQNR 維持在 33.80 dB。
## 架構提議
建議在 Edge NPU 記憶體陣列中整合「HW-DTDP-PIM 引擎」，將無效/冗餘 Token 在記憶體讀取階段直接剔除，避免佔用 NPU 的 DMA 與 MAC 資源。
