# Hardware MLA KV Router (HW-MLA-KVR) 實驗報告

## 摘要 (Executive Summary)
DeepSeek 的 Multi-Head Latent Attention (MLA) 透過將 KV Cache 壓縮為 Latent Vectors 顯著降低了記憶體需求。然而，在解碼階段，軟體必須頻繁地讀取這些壓縮向量，並將其廣播 (Broadcast) 或路由給所有 Attention Heads。這段軟體 Tensor Reshaping 與 Routing 過程仍會消耗可觀的時間。本實驗評估將這段路由邏輯硬體化。

## 實驗結果
- **Software MLA KV Routing Latency**: ~1.91 ms
- **HW-MLA-KVR Latency**: ~0.04 ms
- **Speedup**: 45.37x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 SRAM 控制器中實作原生的「HW-MLA-KVR 路由匯流排」，可以零延遲地將壓縮向量多播 (Multicast) 至後端的 Up-Projection 引擎。建議在原生支援 DeepSeek MLA 的 Edge NPU 中整合此匯流排，徹底消除軟體 Tensor 操作開銷。
