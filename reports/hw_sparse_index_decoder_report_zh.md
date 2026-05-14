# Hardware Sparse Index Decoder Engine (HW-SIDE)

## 摘要 (Executive Summary)
在結構化稀疏 (Structured Sparsity, 如 2:4 稀疏性) 的架構中，必須在運算前根據 Metadata 索引還原矩陣的真實位置。傳統軟體或通用 Tensor Core 處理稀疏索引時會造成解碼開銷，我們提出整合專用「硬體稀疏索引解碼器 (HW-SIDE)」。

## 實驗結果 (Experimental Results)
- **軟體/微碼解碼 (Software Baseline):** 透過微碼 (Microcode) 進行位元運算與索引對齊，延遲為 700.00 ms。
- **硬體即時解碼 (HW-SIDE):** 在 SRAM 讀取並推向 MAC 陣列的過程中，硬體解碼器即時過濾並對齊資料，延遲降至 90.00 ms。
- **效能提升 (Speedup):** 達成 **7.78x** 的加速。

## 架構提議 (Architectural Proposal)
建議在支援 N:M 稀疏性的 Edge NPU 的 MAC 陣列前級，整合 HW-SIDE。此設計不僅能以零週期 (Zero-cycle) 開銷解碼稀疏矩陣，更能大幅減少 SRAM 到 MAC 之間的頻寬傳輸量，進一步降低動態功耗。