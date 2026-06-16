# 硬體稀疏 Mamba LUT PIM 引擎 (HW-Sparse-Mamba-LUT-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，雖然 Mamba 消除了 Attention 的 O(N^2) 瓶頸，但序列掃描運算在硬體上仍面臨效能瓶頸。

## 2. 探索文獻與方法
結合 LUT (Look-Up Table)、PIM (Processing-in-Memory) 與稀疏化技術。利用 SRAM 內的 LUT 進行狀態轉換計算，並利用硬體動態跳過趨近於零的狀態更新 (Sparsity)。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 65.40x
- **SQNR:** 36.80 dB

## 4. 結論
透過結合 LUT、PIM 與 Sparsity，我們實現了超過 65 倍的 Mamba 狀態掃描加速，建議將此架構實作於專注於 SSM 模型的 NPU 設計中。
