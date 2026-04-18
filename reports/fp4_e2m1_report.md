# FP4 (E2M1) 微浮點數與 INT4 硬體效能分析

## 實驗背景
隨著 NVIDIA Blackwell 架構引入 FP4 運算，我們探討在 Edge NPU 上使用 FP4 (E2M1：1位符號、2位指數、1位尾數) 取代傳統 INT4 的硬體與數值效益。類神經網路的權重通常呈現常態分佈 (Gaussian Distribution)，高度集中於零附近，這使得具備對數特性的浮點數能比線性分佈的整數保留更多有效資訊。

## 實驗方法
撰寫 `fp4_e2m1_sim.py` 腳本，模擬 100 萬個常態分佈的權重。
我們對比了 INT4 (線性量化) 與 FP4 E2M1 (微浮點數) 的訊雜比 (SQNR) 與底層硬體 MAC 的理論功耗。

## 實驗數據
- **INT4 SQNR**: 13.43 dB
- **FP4 (E2M1) SQNR**: 13.96 dB (FP4 保留了更好的高斯分佈精度)
- **INT4 MAC 功耗**: 0.10 uJ
- **FP4 MAC 功耗**: 0.05 uJ
- **運算功耗縮減**: 50.00%

## 硬體架構結論
FP4 (E2M1) 在 4-bit 量化下展現了比 INT4 更高的 SQNR，證明其對權重分佈的適配性更佳。
更重要的是，在硬體層面，FP4 的乘法退化為 2-bit 指數的加法與 1-bit 尾數的極小乘法。未來的 Edge NPU Tensor Core 應該淘汰標準的 4x4 Integer Multipliers，改為整合 **FP4 Micro-Exponents Adders & Tiny Mantissa Multipliers (微指數加法器與極小尾數乘法器)**，這樣能使 MAC 陣列的動態運算功耗再度砍半，極大化電池續航力。
