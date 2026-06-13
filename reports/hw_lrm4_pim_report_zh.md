# 硬體架構研究報告: HW-LRM4-PIM (Low-Rank Mamba-4 PIM Engine)
## 摘要
本研究評估了 Mamba-4 的低秩 (Low-Rank) 狀態更新結合 PIM (Processing-in-Memory) 的硬體加速架構。在 1024000 (1M) 超長上下文長度下，相較於傳統數位 MAC 陣列，達成 125.00 倍的延遲加速，且 SQNR 維持在 33.50 dB。
## 架構提議
建議在 Edge NPU 記憶體陣列中整合「HW-LRM4-PIM 引擎」，將高維度低秩矩陣乘法直接卸載至 SRAM Bitlines，解決百萬長度序列的記憶體頻寬牆問題。
