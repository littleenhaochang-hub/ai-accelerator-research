# MoE Content-Addressable Memory (TCAM) 路由硬體

## 實驗背景 (Background)
隨著 Mixture-of-Experts (MoE) 架構向細粒度發展 (如 DeepSeek 的 256+ Experts)，Token 路由 (Routing) 階段的計算成本急劇上升。傳統軟體做法需要計算 Token 與所有 Expert 質心的內積 (Softmax)，再進行 Top-K 排序。這導致 $O(E)$ 的乘加與 $O(E \log E)$ 的排序開銷，嚴重占用 NPU 的計算資源與時間。

## 物理模擬 (Physical Simulation)
透過 `moe_cam_routing_sim.py`，我們比較了傳統 SRAM (MAC + 排序) 與 TCAM (Ternary Content-Addressable Memory) 的路由延遲：
- **傳統 SRAM 路由延遲 (4096 Tokens, 256 Experts)**: 5255.17 ms
- **TCAM 硬體並行路由延遲**: 4.10 ms
- **整體加速比**: 1283.00x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 內部加裝專用的 **「TCAM MoE Router」**。
將各個 Expert 的特徵質心直接寫入 TCAM。當 Token 進入時，TCAM 可以在單一硬體時脈週期內，並行完成所有 Expert 的距離比對與 Nearest-Neighbor 匹配 (O(1) 複雜度)。這不僅徹底消除了 Routing 階段的 MAC 與排序運算，更讓數百個 Expert 的調度達到了近乎「零延遲」的境界。
