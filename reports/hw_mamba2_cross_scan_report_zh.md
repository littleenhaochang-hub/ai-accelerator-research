# Hardware Mamba-2 Cross-Scan Engine (HW-M2CSE) 實驗報告

## 摘要 (Executive Summary)
Mamba-2 透過 SSD (State Space Duality) 改善了平行化能力，但其 Cross-Scan 操作在軟體端依然會遇到大量的記憶體循序讀寫問題。本實驗探索將 Cross-Scan 邏輯硬體化，使用專門的「HW-M2CSE (Cross-Scan Engine)」。

## 實驗結果
- **Software Sequential Scan Latency**: ~0.03 ms
- **HW-M2CSE Latency**: ~0.01 ms
- **Speedup**: 6.82x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，硬體層級的平行掃描樹 (Parallel Scan Tree) 可以有效解除 Mamba-2 Cross-Scan 操作的軟體記憶體瓶頸。我們建議在 Edge NPU 記憶體控制器中加入「HW-M2CSE 引擎」，以硬體線路完成掃描與聚合。
