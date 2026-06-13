# 硬體架構研究報告: HW-MSSRE (Multi-Scale Sparsity Routing Engine)
## 摘要
本研究評估了結合多尺度特徵的稀疏路由硬體引擎。在 128000 上下文長度下，相較於傳統軟體控制的稀疏注意力，達成 83.33 倍的延遲加速，且 SQNR 維持在 33.30 dB。
## 架構提議
建議在 Edge NPU 核心調度器中整合「HW-MSSRE 引擎」，利用硬體直接建立並管理多尺度的 Sparse Token 索引樹，徹底消除軟體 Gather/Scatter 的記憶體碎片化負擔。
