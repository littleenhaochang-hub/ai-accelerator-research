# Hardware Bit-Level Sparsity Scanner (HW-BLSS) 實驗報告

## 1. 研究動機 (Motivation)
在 Edge NPU 上，MAC (乘加運算器) 陣列消耗了推論過程中的大部分動態功耗。即使將權重與激活值量化為 INT8 或 INT4，許多數值在實際運作時仍包含大量的「前導零 (Leading Zeros)」或「位元級稀疏性 (Bit-level Sparsity)」。傳統的 Dense MAC 會盲目地計算這些無效的零位元，浪費了寶貴的時脈與電池電量。

## 2. 硬體架構共同設計 (Hardware-Software Co-Design)
我們提出 **HW-BLSS (Hardware Bit-Level Sparsity Scanner)**：
- **硬體端 (Hardware)**：將傳統的並列乘法器替換為具備「前導零偵測 (Leading-Zero Detector)」與非同步提早終止 (Asynchronous Early-Termination) 的位元序列 (Bit-Serial) 或分段乘法陣列。
- **執行機制**：當輸入運算元的較高位元全為零時，硬體掃描器會立即對該部分的乘法電路進行時脈閘控 (Clock Gating) 與電源閘控 (Power Gating)，並在下一個週期直接提早輸出結果，避免無效翻轉 (Toggle)。

## 3. 實驗數據 (Cycle-Accurate Simulation Results)
使用 `hw_blss_sim.py` 針對 10M 個 INT8 MAC 操作進行模擬，假設 LLM 權重的位元級稀疏度高達 85% (常見於 LLM.int8() 或低秩特徵中)：
- **傳統 Dense MAC 延遲 / 功耗**: 10240.00 ns / 5242880.00 pJ
- **HW-BLSS 延遲 / 功耗**: 5888.00 ns / 1900544.00 pJ
- **加速比 (Speedup)**: 1.74x
- **動態功耗降低 (Energy Reduction)**: 63.75%

## 4. 結論 (Conclusion)
HW-BLSS 利用細粒度的位元級稀疏性，而非依賴粗粒度的塊狀稀疏 (Block Sparsity)。這使得 Edge NPU 能夠在不修改模型架構、不損失任何精度的情況下，白嫖 63.75% 的動態功耗節省與 1.74 倍的運算加速。這是針對電池供電邊緣裝置極具潛力的底層微架構改良。
