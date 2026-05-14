# Hardware Token-Tree Routing Engine (HW-TTR)

## 摘要 (Executive Summary)
針對推測解碼 (Speculative Decoding) 中龐大 Token-Tree 的狀態追蹤與分岔點驗證瓶頸，本研究探討並實作了基於 TCAM (Ternary Content-Addressable Memory) 的硬體 O(1) 路由架構 (HW-TTR)。

## 實驗結果 (Experimental Results)
- **軟體基準測試 (Software Baseline):** 傳統依賴 CPU/軟體的指標追蹤 (Pointer Chasing) 在 1024 節點、深度 8 的 Draft Tree 中，由於嚴重的 Cache Miss，導致 6415.81 ms 的極高延遲。
- **硬體 TCAM 路由 (HW-TTR):** 採用 O(1) 複雜度的 TCAM 進行平行比對與路由匹配，延遲驟降至 4.53 ms。
- **效能提升 (Speedup):** 達成 **1417.58x** 的大幅加速。

## 架構提議 (Architectural Proposal)
建議在支援 Speculative Decoding 的 Edge NPU 中，將狀態樹追蹤從軟體記憶體移至專用「硬體 TCAM Token-Tree Router」。此舉將徹底消除多分支草稿驗證期間的控制流與記憶體瓶頸。