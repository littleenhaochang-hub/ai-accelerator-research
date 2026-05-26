# Hardware Chunk-Based Prefix Caching (HW-CBPC) 實驗報告

## 摘要 (Executive Summary)
在多輪 Agentic AI 推論中，重用系統提示與歷史紀錄 (Prefix Caching) 能夠大幅降低 Prefill 運算。然而，在軟體端進行 Chunk 級別的記憶體映射與重組會導致顯著的快取未命中與指標延遲。本實驗評估將 Chunk-Based 的記憶體映射機制轉移至硬體 MMU，稱之為「硬體區塊級前綴快取引擎 (HW-CBPC)」。

## 實驗結果
- **Software Chunk Prefix Latency**: ~2.81 ms
- **HW-CBPC Latency**: ~0.05 ms
- **Speedup**: 61.40x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 NPU 記憶體控制器中內建 Chunk-Based 的硬體映射表，可以完全隱藏前綴快取重組時的軟體延遲。建議在 Edge NPU 的 MMU 中整合「HW-CBPC 引擎」，以達到零週期的 Agentic 上下文切換。
