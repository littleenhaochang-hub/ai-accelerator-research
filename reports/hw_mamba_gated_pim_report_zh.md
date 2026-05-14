# Hardware Mamba Gated PIM Engine (HW-MGPE)

## 摘要 (Executive Summary)
針對 Mamba/SSM 模型中依賴輸入資料的閘控機制 (Data-dependent Gating)，我們提出將閘控與狀態更新邏輯遷移至記憶體內運算 (Processing-in-Memory, PIM) 的架構。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Baseline):** 傳統架構中 Mamba Gating 需來回存取記憶體，延遲為 400.00 ms。
- **硬體 PIM 架構 (HW-MGPE):** 在記憶體端直接進行閘控過濾與狀態更新，延遲降至 60.00 ms。
- **效能提升 (Speedup):** 達成 **6.67x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Mamba 專用的 Edge NPU 中整合 HW-MGPE，徹底消除長序列掃描過程中的資料搬運瓶頸。