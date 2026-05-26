# Hardware Context-Aware Dynamic Sparsity (HW-CADS) 實驗報告

## 摘要 (Executive Summary)
在處理超長文本 (Long Context) 時，動態稀疏注意力 (Dynamic Sparse Attention) 是降低運算量的核心。然而，在軟體層面動態評估每個區塊 (Block) 的重要性會產生巨大的 CPU/GPU 同步與控制流延遲。本實驗評估將區塊重要性評估移至硬體層級的「硬體上下文感知動態稀疏引擎 (HW-CADS)」。

## 實驗結果
- **Software Dynamic Sparsity Latency**: ~3.50 ms
- **HW-CADS Latency**: ~0.05 ms
- **Speedup**: 68.73x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 SRAM 讀取端口部署硬體平行的評估器，可以在零軟體開銷下動態略過低重要性的注意力區塊。建議在 Edge NPU 中整合「HW-CADS 引擎」，以硬體原生加速長文本動態稀疏推論。
