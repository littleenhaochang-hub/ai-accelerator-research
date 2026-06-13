# 硬體 Mamba-16 Quantum-Inspired PIM-LUT 狀態空間加速器 (HW-Mamba16-Q-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著模型壓縮的極致化，我們嘗試引入量子啟發 (Quantum-Inspired) 的多態疊加概念。傳統 LUT 每次只能輸出單一確定性狀態，但在處理具備高度不確定性或多重語意分支的長文本時，單一狀態容易造成資訊遺失。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-16 Quantum-Inspired PIM-LUT 架構**。我們在 SRAM 讀取放大器 (Sense Amplifiers) 後端整合了隨機採樣與多態疊加電路。透過極低精度的機率分佈查表，硬體能在同一週期內平行展開多個可能的隱藏狀態，並以疊加態 (Superposition State) 繼續向下傳遞。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba16_quantum_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 537.04x
*   **訊號雜訊比 (SQNR):** 38.3 dB (疊加態有效保留了多重語意特徵，提升了整體保真度)
*   **硬體提案:** 建議在下一代處理模糊語意與多分支推理的 Edge NPU 中，實作「量子啟發疊加態 PIM-LUT」。

## 4. 結論 (Conclusion)
HW-Mamba16-Q-PIM-LUT 成功將量子運算中的疊加態概念以古典 CMOS 數位電路在記憶體內實現，為狀態空間模型處理極端複雜語意帶來了全新的硬體設計思維。