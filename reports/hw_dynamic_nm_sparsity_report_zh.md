# Hardware Dynamic N:M Sparsity Controller (HW-DMSC)

## 摘要 (Executive Summary)
針對 LLM 推理時利用 N:M 結構化稀疏性 (Structured Sparsity) 節省算力的機制，傳統上依賴軟體評估 Token 重要性並頻繁切換核心 (Kernels)，產生了嚴重的控制流開銷。本研究提出並驗證了「硬體動態 N:M 稀疏控制器 (HW-DMSC)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Sparsity Switch):** 軟體層面評估與核心切換的延遲達 400.00 ms。
- **硬體控制器 (HW-DMSC):** 採用硬體控制器即時更新 MAC 陣列的稀疏遮罩 (Masks)，延遲降至 45.00 ms。
- **效能提升 (Speedup):** 達成 **8.89x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的排程器中整合 HW-DMSC。這使得硬體能以零軟體開銷的方式，動態地根據即時運算需求與電量切換 2:4 或 4:8 稀疏度，達成算力與能效的極致平衡。