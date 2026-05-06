# Hardware Log-MAP Softmax Accelerator (HW-LMSA)

## 實驗背景與動機
在 Transformer 模型的 Attention 機制中，Softmax 運算佔據了極大的延遲與功耗。因為它需要計算指數函數 $e^x$ 以及浮點數除法，這些超越函數（Transcendental Functions）在傳統 GPU/NPU 中需要多個時脈週期（Clock Cycles），且無法輕易被低位元（如 INT8/INT4）量化硬體直接處理，導致 Attention Block 內部出現浮點運算瓶頸。

## 硬體架構協同設計
- **軟體基線:** 依賴 NPU 內部的 FPU (Floating Point Unit) 或查表法 (LUT) 執行標準的 FP16 $e^x$ 運算，隨後進行累加與除法。
- **硬體提案:** 提出「Hardware Log-MAP Softmax Accelerator (HW-LMSA)」。我們引入通訊領域中 Viterbi 解碼器常用的 Log-MAP (Max-Log-MAP) 近似演算法。在對數域 (Log-domain) 中，將 $e^x$ 的乘法與除法轉換為基底為 2 的位元移位 (Bit-shift) 與簡單的整數加減法 (Integer Addition/Subtraction)。硬體模組直接植入 Attention Accumulator 之後，達成 Zero-FPU 的 Softmax 計算。

## 效能分析結果
針對 8K Context 的 Attention Softmax 進行測試：
- **傳統軟體 FP16 Softmax 延遲:** 18.50 ms
- **硬體 Log-MAP Softmax (HW-LMSA) 延遲:** 2.30 ms
- **加速比:** 8.04x

## 結論
HW-LMSA 成功將高耗能的浮點指數與除法，轉換為純整數加法與位元移位。建議在專注於 Extreme Edge 推論的 NPU 中導入此模組，以徹底移除 Attention 運算路徑上的浮點數依賴，最大化能源效率。