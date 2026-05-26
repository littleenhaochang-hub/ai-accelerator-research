# Hardware GQA Crossbar Router (HW-GQA-CR) 實驗報告

## 摘要 (Executive Summary)
Grouped-Query Attention (GQA) 透過多個 Query 共享同一個 KV Head 來減少記憶體頻寬，但在軟體端需要進行指標映射與資料複製。本實驗評估了將 GQA 路由邏輯移至硬體 Crossbar Switch (HW-GQA-CR) 的效益，實現零週期的資料廣播。

## 實驗結果
- **Software GQA Routing Latency**: ~0.06 ms
- **HW-GQA-CR Latency**: ~0.01 ms
- **Speedup**: 5.82x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，使用硬體 Crossbar Router 可以大幅減少軟體端分配 KV Head 給多個 Query 的延遲。我們建議在 Edge NPU 的 Attention Block 內部整合「硬體 GQA Crossbar Router (HW-GQA-CR)」，利用 SRAM 的多播 (Multicast) 能力，徹底消除 GQA 執行時的軟體路由開銷。
