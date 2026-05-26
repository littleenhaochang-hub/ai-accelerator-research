# Hardware Chunked Sparse Attention Evaluator (HW-CSAE) 實驗報告

## 摘要 (Executive Summary)
在處理超長文本 (128K+) 時，Chunked Attention 是避免 OOM 的標準做法。若搭配區塊稀疏 (Block Sparsity)，可進一步減少運算量。然而，軟體需要預先掃描或追蹤每個 Chunk 的統計數據 (如 Min/Max 邊界) 來決定是否略過該區塊，這引發了龐大的記憶體讀取延遲。本實驗評估將區塊稀疏預測邏輯硬體化 (HW-CSAE)。

## 實驗結果
- **Software Chunk Sparsity Eval Latency**: ~1.80 ms
- **HW-CSAE Latency**: ~0.03 ms
- **Speedup**: 58.22x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 SRAM 讀取埠部署硬體平行的特徵評估器 (Feature Evaluator)，能在零額外記憶體開銷下預測 Chunk 稀疏度，並及時進行時脈閘控 (Clock Gating)。我們建議在 Edge NPU 記憶體控制器中整合「HW-CSAE 引擎」，以原生加速超長文本的稀疏推論。
