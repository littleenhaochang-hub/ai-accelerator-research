# SiLU / SwiGLU 非線性激勵函數硬體近似分析

## 實驗背景
現代 LLM (如 LLaMA, DeepSeek) 廣泛採用 SwiGLU 作為 FFN 層的激勵函數，其底層依賴 SiLU ($x \cdot \sigma(x)$)。在硬體層面，精確計算 Exponential (exp) 與 Division 非常耗費面積與功耗，是 Tensor Core 之外的一大能耗瓶頸。

## 實驗方法
撰寫 `silu_approximation_sim.py`，模擬 1.34 億個元素的激勵向量運算。
我們比較了需要複雜浮點運算的「精確 SiLU」與使用 Piecewise Linear (PWL) 分段線性逼近的「近似 SiLU」在功耗上的差異，並計算其 SQNR。

## 實驗數據
- **Baseline (Exact Exp) Energy**: 2013.27 uJ
- **PWL Approximation Energy**: 201.33 uJ
- **Energy Reduction**: 90.00%
- **Approximation SQNR**: 24.49 dB (足夠維持大模型推論精度)

## 硬體架構結論
透過 Piecewise Linear (PWL) 近似，SiLU 激勵函數的運算功耗能大幅降低 **90%**，同時維持約 24.5 dB 的 SQNR，這對 W4A4 模型來說已遠超出量化雜訊的底線。
未來的 Edge NPU 不應該實作複雜的超越函數 (Transcendental Function) 單元，而是應該在 FFN 的資料路徑上實作 **PWL/LUT Activation Engine (分段線性/查表激勵引擎)**，以極低的面積與功耗成本執行所有的非線性激勵運算。
