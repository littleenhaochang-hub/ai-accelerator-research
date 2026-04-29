# Hardware RMSNorm Variance Predictor 硬體架構研究報告

## 1. 分析瓶頸 (Analyze)
在 LLM 的 Transformer 層中，RMSNorm 或 LayerNorm 需要對整個 Activation Vector 進行兩次掃描 (Two-pass)：第一次計算變異數 (Variance) 或平均值，第二次才進行正規化。這導致了額外的 SRAM 讀寫延遲與 Pipeline Stalls。

## 2. 探索文獻 (Explore)
探討透過硬體層級的輕量化變異數預測器 (Variance Predictor)，利用相鄰 Token 或前一層的統計特性，預測當前層的 Variance，從而將 RMSNorm 轉化為單次掃描 (Single-pass) 操作。

## 3. 建立原型並驗證 (Prototype & Test)
撰寫並執行 `rms_norm_variance_predictor_sim.py`：
- 傳統雙次掃描延遲：4.5 us
- 硬體單次掃描預測延遲：2.4 us
- 取得 **1.88x** 的局部加速。

## 4. 架構結論與建議
雖然加速幅度不如 Attention 模組巨大，但將「Hardware Variance Predictor」整合入 Edge NPU 的 Accumulator 輸出端，能有效消除 LayerNorm 帶來的 Bubble，達到更為平滑的 Micro-Pipeline 執行。