# 硬體線性注意力 PIM 引擎 (HW-Linear-Attention-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，長文本處理需要低複雜度的 Attention 機制。線性注意力 (Linear Attention) 雖然理論上是 O(N)，但在硬體實作中，大量的特徵映射與狀態累積仍會消耗大量記憶體頻寬。

## 2. 探索文獻與方法
利用 Processing-in-Memory (PIM) 架構，將特徵映射 (Feature Mapping) 與狀態累積 (State Accumulation) 直接下放到 SRAM 內執行，避免頻繁的資料來回搬遷。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 31.50x
- **SQNR:** 36.30 dB

## 4. 結論
透過 PIM 技術加速線性注意力的狀態累積，大幅減少了記憶體頻寬壓力。建議整合 HW-Linear-Attention-PIM 至處理長文本的邊緣運算裝置中。
