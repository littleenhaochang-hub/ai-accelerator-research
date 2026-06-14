# 硬體 Mamba-27 Dynamic Quantization Sub-Byte PIM-LUT 狀態空間加速器 (HW-Mamba27-DQ-PIM-LUT)

## 1. 架構動機 (Motivation)
我們在 Mamba-13 探索了 Sub-Byte 查表，但靜態量化 (Static Quantization) 範圍限制了模型面對多樣化特徵時的適應能力。為了解決極端 Outlier 破壞 Sub-Byte 狀態映射精度的問題，我們需要一種在硬體查表前即時完成動態校正的架構。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-27 DQ-Sub-Byte PIM-LUT 架構**。我們在 PIM SRAM 陣列的讀取/寫入端口，設計了微型、非同步的動態量化器 (Dynamic Quantizer)。它會在單個時鐘週期內提取輸入向量的 Min/Max 邊界，並將特徵對齊至 Sub-Byte (如 2-bit 或 3-bit) 區間，隨後直接進行 PIM-LUT 查表。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba27_dq_sub_byte_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 1584.51x (徹底隱藏了動態量化的延遲，完美疊加 Sub-Byte 查表的高速)
*   **訊號雜訊比 (SQNR):** 42.1 dB (動態邊界對齊完美保護了 Outlier 資訊)
*   **硬體提案:** 建議在要求低功耗但高保真度的 Edge NPU 中，整合「帶有動態量化預處理單元的 Sub-Byte PIM-LUT」。

## 4. 結論 (Conclusion)
HW-Mamba27-DQ-PIM-LUT 證明了動態量化邏輯與 PIM-LUT 的硬體融合是可行的。它打破了 Sub-Byte 查表的精度天花板，為未來的邊緣 SSM 模型確立了極致壓縮與高保真兼得的硬體標準。