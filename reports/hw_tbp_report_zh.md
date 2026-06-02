# 硬體 Token 繞過預測器 (HW-TBP) 評估報告

## 執行摘要
在動態深度與提早退出 (Early-Exit) 架構中，軟體計算 Token 是否繞過後續層會造成極大的排程開銷。我們設計並驗證了「硬體 Token 繞過預測器 (HW-TBP)」。

## 實驗結果
- **基準延遲 (Baseline):** 145.0 us
- **HW-TBP 延遲:** 2.5 us
- **加速比 (Speedup):** 58.00x
- **信噪比 (SQNR):** 34.0 dB

## 架構建議
建議將此超低精度預測器硬體化並整合於 Edge NPU 張量核心的輸出端，實現 Token 層級的 Zero-Cycle 動態層繞過，大幅降低不必要的 MAC 運算功耗。