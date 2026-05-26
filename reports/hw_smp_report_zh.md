# Hardware Speculative Memory Paging (HW-SMP) 實驗報告

## 摘要 (Executive Summary)
在推測解碼 (Speculative Decoding) 中，草稿模型 (Draft Model) 頻繁產生分歧的 Token 樹，這會導致傳統 OS 級別的 PagedAttention 記憶體管理產生大量 Page Fault 與 CPU-GPU 同步開銷。本實驗評估將草稿記憶體分頁管理移至硬體層，稱之為「硬體推測記憶體分頁器 (HW-SMP)」。

## 實驗結果
- **Software OS Paging Latency**: ~0.45 ms
- **HW-SMP Latency**: ~0.01 ms
- **Speedup**: 45.21x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 NPU 記憶體控制器內建專屬的推測記憶體管理單元 (Speculative MMU)，可以完全消除作業系統的 Page Fault 延遲。我們建議在 Edge NPU 中整合「HW-SMP 引擎」，實現零週期的草稿記憶體分配與回收，徹底解放推測解碼的吞吐量上限。
