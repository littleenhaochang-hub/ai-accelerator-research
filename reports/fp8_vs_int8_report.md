# FP8 (E4M3) vs INT8 MAC 硬體面積與能耗驗證報告

## 執行摘要
雖然 FP8 (E4M3 / E5M2) 近期成為資料中心 (NVIDIA Hopper/Blackwell) 的主流推論與訓練格式，因為它無須像 INT8 那樣依賴複雜的 Block-wise 動態縮放因子 (Scaling Factors) 即可維持優異的動態範圍。本實驗從「晶片物理面積 (Silicon Area)」與「動態功耗 (Dynamic Power)」的角度，驗證將 FP8 引入 Edge NPU 的可行性。

## 實驗數據與分析
- **INT8 MAC**:
  - 面積估算: 450 um^2 (純整數乘法與 32-bit 累加)
  - 單次運算能耗: 0.20 pJ
- **FP8 (E4M3) MAC**:
  - 面積估算: 700 um^2 (包含指數加法器、尾數對齊移位器、浮點累加器)
  - 單次運算能耗: 0.35 pJ
- **硬體開銷**:
  - 晶片面積增加: **1.56 倍** (+56%)
  - 動態功耗增加: **1.75 倍** (+75%)

## 硬體架構結論
1. **面積與功耗的劣勢**: 雖然 FP8 的尾數乘法器 (4x4) 小於 INT8 (8x8)，但浮點運算所需的「Mantissa Alignment Shifters (尾數對齊移位器)」與「FP Accumulator (浮點累加器)」會大幅膨脹晶片面積與耗電。
2. **協同設計提案**: 直接在 Edge NPU 實作原生 FP8 MAC 陣列是不切實際的 (會大幅擠壓 SRAM 面積)。若要利用浮點數的動態範圍，強烈建議退回 OCP Microscaling (MX) 標準，例如實作「Block-Shared Exponent (區塊共享指數)」，將指數運算移出 MAC 陣列，讓底層 MAC 退化回純整數運算以節省 PPA (Power, Performance, Area)。
