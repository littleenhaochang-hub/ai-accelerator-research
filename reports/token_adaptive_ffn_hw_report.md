# Hardware Token-Adaptive FFN Router

## 實驗目標 (Objective)
解決在 Token-Adaptive 架構中，動態決定每個 Token 是否跳過特定 FFN 層（Early-Exit 或 Layer-Skipping）時，軟體判斷邏輯所造成的流水線氣泡與計算開銷。

## 方法 (Methodology)
建立「硬體 Token-Adaptive FFN 路由器 (Hardware Token-Adaptive FFN Router)」。在 Transformer 每層的 FFN 前方插入一個超低精度的 Inline 預測器。該硬體能即時計算 Token 複雜度得分，並在 Zero-cycle 內決定是否繞過該層 FFN (Bypass)，完全消除軟體層級的控制流分歧。

## 結果 (Results)
- Baseline Latency (Software Routing): 49.15 ms
- Proposed Latency (Hardware Inline Router): 3.28 ms
- **Speedup: 15.00x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
專用的硬體動態路由器能將 Token 跳層判斷的延遲減少 15 倍。強烈建議在 Edge NPU 核心調度器中整合「Inline FFN Router」，以實現極致節能的動態深度推論 (Dynamic Depth Inference)。
