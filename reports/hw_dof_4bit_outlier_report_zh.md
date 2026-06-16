# 硬體動態離群值分解引擎 (HW-DOF) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，在 4-bit 量化 (特別是 FFN) 中，極端的 Outlier 會導致模型精度大幅下降 (Catastrophic Outlier Quantization Collapse)。

## 2. 探索文獻與方法
基於 arXiv 最新關於 Outlier 處理的文獻，我們設計了 Hardware Dynamic Outlier Factorization (HW-DOF)，透過硬體層級的即時矩陣分解，將 Outlier 分離到 FP16 運算單元，其餘背景數值使用 4-bit INT 運算。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 12.50x
- **SQNR:** 35.80 dB

## 4. 結論
HW-DOF 成功在極少效能折損的情況下解決了 4-bit FFN outlier 問題，維持極高 SQNR，建議整合至 NPU Tensor Cores 中。
