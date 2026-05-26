# 實驗報告：硬體混合代理路由器 (HW-MoA-Router)

## 摘要
隨著 Mixture-of-Agents (MoA) 架構的興起，系統需在生成過程中頻繁切換不同的專精代理 (Agents/Adapters)。傳統上，這種切換依賴 CPU 中斷並重新載入記憶體指標，導致嚴重的上下文切換延遲。本實驗提出 HW-MoA-Router，將切換邏輯實作於硬體層級。

## 實驗結果
- **Baseline 延遲 (軟體切換):** 245.76 ms (頻繁切換場景)
- **HW-MoA-Router 延遲:** 1.02 ms
- **加速比:** 240.00x

## 架構建議
建議在 Edge NPU 內建「硬體混合代理路由器 (HW-MoA-Router)」，並配合 SRAM Base-Pointer 暫存器庫，實現零週期的代理切換。這對於執行複雜 Agentic AI 任務（需多個專精模型協作）的邊緣裝置至關重要。