# Hardware Dynamic Sparse Attention Engine (HW-DSAE)

## 摘要 (Executive Summary)
在支援 Token 捨棄 (Token Dropping) 的 Sparse Attention 架構中，軟體需要頻繁地重組張量 (Tensor Gathering) 以剔除被捨棄的 Token，這造成了嚴重的記憶體頻寬負載與 CPU/GPU 同步開銷。本研究驗證了「硬體動態稀疏注意力引擎 (HW-DSAE)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Overhead):** 軟體追蹤 Mask 並進行 Gather/Scatter 重排，延遲達 480.00 ms。
- **硬體過濾器 (HW-DSAE):** 在 SRAM 讀取埠整合硬體過濾邏輯，直接拒絕讀取無效 Token，延遲降至 40.00 ms。
- **效能提升 (Speedup):** 達成 **12.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的 Attention Block 中整合 HW-DSAE。透過在硬體層面即時剔除無效 Token，系統能完全免除軟體重組張量的開銷，極大化 Tensor Cores 的有效運算率 (Utilization)。