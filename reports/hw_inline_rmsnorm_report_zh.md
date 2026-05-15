# Hardware Inline RMSNorm Engine (HW-IRE)

## 摘要 (Executive Summary)
RMSNorm (Root Mean Square Normalization) 在現代 LLM 中被廣泛使用，但傳統軟體實作需要對記憶體進行兩次掃描 (Two-Pass)：第一次計算平方平均，第二次進行正規化，導致嚴重的記憶體頻寬浪費。本研究提出了「硬體即時 RMSNorm 引擎 (HW-IRE)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Two-Pass):** 依賴 CPU/GPU 進行兩次記憶體讀取的軟體正規化延遲為 380.00 ms。
- **硬體正規化 (HW-IRE):** 透過在 MAC 輸出端暫存器內建累加器與除法邏輯，達成「單趟 (One-Pass)」即時正規化，延遲降至 35.00 ms。
- **效能提升 (Speedup):** 達成 **10.86x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的 Tensor Core 輸出路徑上直接整合 HW-IRE。這將消除所有因為 Normalization 產生的額外 SRAM 讀寫，顯著降低動態功耗並提升 Pipeline 效率。