# Hardware Token Compactor Engine (HW-TCE)

## 摘要 (Executive Summary)
針對 Token Pruning (動態 Token 丟棄) 與 Token Merging (ToMe) 演算法，被丟棄的 Token 會在記憶體中留下「碎片 (Bubbles)」，導致後續 Tensor 運算需要軟體執行昂貴的 Gather/Scatter 記憶體重整。我們提出在 SRAM 介面整合「硬體 Token 壓縮器 (HW-TCE)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Pruning):** 依賴 CPU/GPU 軟體核心進行 Indexing 與記憶體複製重整，延遲為 550.00 ms。
- **硬體壓縮 (HW-TCE):** 透過硬體 DMA 引擎在資料寫入 SRAM 的當下即時過濾並連續擺放 (Compaction)，延遲降至 60.00 ms。
- **效能提升 (Speedup):** 達成 **9.17x** 的加速。

## 架構提議 (Architectural Proposal)
建議在支援動態深度 (Dynamic Depth) 或動態稀疏性的 Edge NPU 記憶體控制器中，直接整合 HW-TCE。此設計能保證 MAC 陣列永遠接收連續的資料流，將演算法層面的 FLOPs 節省，完美轉化為硬體層面的真實加速。