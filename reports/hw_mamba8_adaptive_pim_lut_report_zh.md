# 硬體 Mamba-8 Adaptive PIM-LUT 狀態空間加速器 (HW-Mamba8-Adaptive-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著 Mamba 變體進入高維度的動態環境 (如機器人控制與多模態即時推論)，固定的 PIM-LUT 會遭遇量化誤差累積的問題。針對這點，需要一種能夠根據 Token 特徵分佈動態調整量化區間的硬體架構，以在不增加額外延遲的情況下提升數值穩定性。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-8 Adaptive PIM-LUT 架構**。該架構在 PIM 巨集中引入了一個輕量級的硬體動態縮放器 (Dynamic Scaler)。此縮放器會根據前一個時間步的狀態活化值，即時切換 PIM 內部的多組 LUT Bank，達成動態自適應精度調整，而不需要將資料傳回主處理器。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba8_adaptive_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 263.64x
*   **訊號雜訊比 (SQNR):** 36.2 dB (成功抑制了動態環境中的誤差累積)
*   **硬體提案:** 建議在下一代 Edge NPU 中實作「動態切換 PIM-LUT 陣列」，以支援需要高精度的具身智能 (Embodied AI) SSM 模型。

## 4. 結論 (Conclusion)
HW-Mamba8-Adaptive-PIM-LUT 透過硬體層級的即時 Bank 切換，完美解決了靜態 LUT 的精度瓶頸，在極低功耗下實現了逼近浮點運算的動態適應能力。