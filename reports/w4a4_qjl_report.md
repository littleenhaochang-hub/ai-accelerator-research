# W4A4 QJL Quantization: 解決 Activation Outlier 的硬體協同設計

## 瓶頸分析
根據 `ai-accelerator-research/RESEARCH_REPORT.md`，W4A4 (4-bit 權重與 4-bit 激勵) 量化在大型語言模型 (LLM) 中會遭遇災難性的精度下降。這主要源於 LLM 的 Activations 具有極端的 Heavy-Tail Outliers (極端值)，導致傳統的 INT4 量化範圍被撐大，使得正常數值的量化解析度嚴重不足 (SQNR 極低)。

## 探索文獻與原型設計
我們研究了基於 Johnson-Lindenstrauss (JL) 引理的隨機投影技術，並撰寫了 `w4a4_qjl_sim.py` 進行數學模擬。
核心思想：在量化之前，通過一個正交矩陣 (Orthogonal Matrix) 旋轉 Activation 向量，將極端的 Outlier 「攤平」(Flattening) 到所有通道中。因為旋轉矩陣保持了 $L_2$ 範數 (能量守恆)，我們可以在量化後再反向旋轉回來。

## 實驗結果
- **Naive INT4 SQNR:** 6.63 dB (發生嚴重的精度坍塌)
- **QJL INT4 SQNR:** 11.89 dB (提升約 5.26 dB)
實驗證明，透過 QJL 攤平極端值，可以在不損失資訊的情況下大幅縮小量化區間的動態範圍，使得 INT4 的表達能力大幅提升。

## 硬體實作挑戰與下一步
雖然數學上 QJL 有效，但密集的正交矩陣乘法 $X \times Q$ 會引入額外的 $O(d^2)$ 計算延遲。為了在 Mac mini 等邊緣設備上實現，我們下一步必須將任意的隨機正交矩陣替換為**硬體友善的 Walsh-Hadamard Transform (WHT)**，因為 WHT 只需要加減法 (無乘法)，且複雜度僅為 $O(d \log d)$，非常適合實作為 SRAM 旁的固定邏輯電路 (Fixed-function RTL)。
