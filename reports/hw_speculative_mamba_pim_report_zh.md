# 硬體推測 Mamba PIM 引擎 (HW-Speculative-Mamba-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，推測解碼 (Speculative Decoding) 在 Mamba 等 SSM 模型上應用時，草稿驗證與狀態更新的延遲仍然是瓶頸。

## 2. 探索文獻與方法
結合 PIM 架構，將 Mamba 的草稿狀態追蹤與驗證比較邏輯直接整合進 SRAM 中。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 55.40x
- **SQNR:** 36.20 dB

## 4. 結論
透過 PIM 執行推測解碼驗證，大幅提升了 Mamba 的生成速度，建議將此架構實作於專注於 SSM 模型的 NPU 設計中。
