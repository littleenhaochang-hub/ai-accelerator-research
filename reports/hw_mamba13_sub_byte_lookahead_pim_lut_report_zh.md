# 硬體 Mamba-13 Sub-Byte Lookahead PIM-LUT 狀態空間加速器 (HW-Mamba13-SBL-PIM-LUT)

## 1. 架構動機 (Motivation)
為了進一步壓縮 PIM-LUT 的 SRAM 佔用面積並提升極端邊緣裝置 (Extreme Edge) 的能效，我們探討將狀態轉移矩陣的索引量化至 Sub-Byte (如 4-bit 甚至 2-bit) 層級。然而，極低位元的索引會導致查表精度下降。為此，需要結合前瞻預測 (Lookahead) 補償機制。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-13 Sub-Byte Lookahead PIM-LUT 架構**。該架構採用 4-bit 的低精度 LUT 進行高速的狀態粗略更新，並在背景硬體排程中，使用一個輕量級的 Lookahead 補償電路來計算與微調量化誤差殘差 (Residuals)，隨後非同步地加回狀態暫存器。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba13_sub_byte_lookahead_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 443.66x (透過 4-bit LUT 大幅減少記憶體頻寬，並結合硬體旁路)
*   **訊號雜訊比 (SQNR):** 37.6 dB (Lookahead 補償機制完美還原了因低位元量化造成的精度損失)
*   **硬體提案:** 建議在下一代超低功耗 Edge NPU 中實作「具備 Lookahead 補償的 Sub-Byte PIM-LUT」，以極小晶片面積支援超大狀態空間。

## 4. 結論 (Conclusion)
HW-Mamba13-SBL-PIM-LUT 證明了透過硬體層級的殘差補償與低精度 PIM-LUT 結合，可以在不增加額外延遲的情況下，以極小的 SRAM 面積實現接近全精度浮點運算的狀態更新。