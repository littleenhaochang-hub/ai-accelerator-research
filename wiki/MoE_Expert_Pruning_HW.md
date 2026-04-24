# Hardware MoE Expert Pruner (硬體 MoE 專家動態剪枝器)

## 實驗背景 (Background)
在大規模 MoE 架構中，許多 Expert 獲得的路由機率極低，對最終輸出的貢獻微乎其微。若能動態「剪枝 (Pruning)」這些低機率的 Expert，可以大幅節省 DRAM 的讀取頻寬。然而，在軟體層面執行 Masking 與閾值判斷，會引入大量耗時的 Control-flow (控制流) 分支指令，拖累 Routing 階段的效能。

## 物理模擬 (Physical Simulation)
透過 `moe_expert_pruning_hw_sim.py`，比較了軟體層 Masking 與硬體即時剪枝引擎的效能差距：
- **軟體專家剪枝延遲 (4096 Tokens, 128 Experts)**: 2621.44 ms
- **硬體即時專家剪枝延遲**: 157.29 ms
- **整體加速比**: 16.67x

## 架構提案 (Architectural Proposal)
提議在 MoE Router ALU 的輸出端加裝 **「Inline Logit Threshold Pruner」**。
在 Router 計算出機率分佈的瞬間，硬體比較器 (Comparator) 會即時將低於設定閾值的 Expert 分數歸零，並將其從執行佇列中剔除。這項設計以「零時脈週期 (Zero-cycle)」的代價完成了動態剪枝，徹底阻斷了 DMA 去抓取無用權重的行為，為 Edge NPU 節省了龐大的頻寬與功耗。
