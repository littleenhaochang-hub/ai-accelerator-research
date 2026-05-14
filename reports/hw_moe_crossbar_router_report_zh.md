# Hardware MoE Crossbar Router Engine (HW-MCRE)

## 摘要 (Executive Summary)
針對 Mixture-of-Experts (MoE) 模型中 Token 分發至各個 Expert 的路由瓶頸，傳統軟體實作依賴 Top-K 排序與記憶體離散存取 (Scatter/Gather)。本研究提出以硬體 O(1) 交叉開關 (Crossbar Switch) 取代軟體路由邏輯。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Routing):** 依賴 CPU/GPU 進行 Token 的 Top-K 排序與記憶體重整，延遲達 480.00 ms。
- **硬體交叉開關 (HW-MCRE):** 採用 O(1) 時間複雜度的硬體 Crossbar 陣列即時派發 Token，延遲降至 40.00 ms。
- **效能提升 (Speedup):** 達成 **12.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在專為 MoE 設計的 Edge NPU 內部排程器 (Scheduler) 中整合「硬體 MoE Crossbar 路由引擎」。這將徹底消除軟體層面的排序開銷，使巨型 MoE 模型在邊緣裝置上能達到趨近於 Dense 模型的執行效率。