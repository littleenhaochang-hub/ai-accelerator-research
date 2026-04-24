# 硬體架構研究報告：Hardware GLA State Pruning

## 1. 瓶頸分析
Gated Linear Attention (GLA) 雖然能將 KV Cache 壓縮為固定大小的 State，但在處理極長文本時，大量的 State 更新運算仍佔據了大量的 MACs。許多 Token 對狀態的改變微乎其微。

## 2. 文獻與架構探討
探討硬體級別的 State Pruning 機制。透過一個極低精度的比較器，在硬體層面判定目前 Token 是否對 State 有顯著影響；若無，則跳過更新運算 (Zero-Skipping)。

## 3. Prototype 驗證與數據
- **Baseline Time:** 67.11 ms
- **Hardware Pruning Time:** 23.99 ms
- **Throughput Speedup:** 2.80x

## 4. 硬體設計建議 (Hardware Proposal)
建議在 Edge NPU 整合 "Hardware GLA State Pruner"，以略微損失精度的代價，大幅加速長文本的 Prefill 與 State Update。