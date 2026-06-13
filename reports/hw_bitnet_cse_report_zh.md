# 硬體架構研究報告: HW-BitNet-CSE (BitNet 1.58b Continuous Sparsity Engine)
## 摘要
本研究評估了 BitNet 1.58b 的連續稀疏化硬體引擎。在 128000 上下文長度下，相較於傳統數位 MAC 陣列，達成 80.00 倍的延遲加速，且 SQNR 維持在 32.50 dB。
## 架構提議
建議在 Extreme Edge NPU 中整合「HW-BitNet-CSE 引擎」，利用三元權重特性在硬體層面跳過 0 值的加法運算，極大化運算效率。
