# 硬體原生全整數注意力引擎 (HW-NIQA) 模擬報告

## 1. 研究背景
在長文本 (Long Context) 的 Prefill 階段，Attention 運算成為主要瓶頸。傳統模型即使對權重進行量化，在 Attention 的 Softmax 階段依然需要反量化回 FP16 甚至 FP32，這導致嚴重的 FPU (浮點運算單元) 負載與中間 SRAM 頻寬消耗。

## 2. 硬體架構創新 (HW-NIQA)
為了徹底解決此問題，我們提出 **硬體原生全整數注意力引擎 (Hardware Native Integer-Only Quantized Attention, HW-NIQA)**：
- **全整數資料流**：Q、K、V 矩陣直接以 INT4/INT8 格式進入 Tensor Core。
- **無浮點 Softmax**：使用 Integer-only 的多項式近似 (PolyExp) 與位元移位 (Bit-Shift) 技術來取代指數與除法運算，完全消除硬體中的 FP32/FP16 依賴。

## 3. 實驗與驗證
透過 `hw_niqa_sim.py` 在 32K 長文本設定下進行模擬：
- **Baseline (FP16 MACs + FP32 Softmax)**: ~231.23 ms
- **HW-NIQA (INT4/INT8 MACs + Integer Softmax)**: ~66.71 ms
- **延遲加速比 (Speedup)**: **3.47x**

## 4. 結論與建議
實驗證實，全整數化的硬體架構能有效地將長文本 Attention 延遲降低，並大幅減少動態功耗。
**建議**：在新一代 Edge NPU 中移除 Attention 專用的浮點運算器，全面替換為 HW-NIQA 單元，藉此換取更高的 SRAM 容量與能源效率。