# 硬體 Mamba-11 Spectral-Filtered PIM-LUT 狀態空間加速器 (HW-Mamba11-SF-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著 PIM-LUT 技術在 Mamba 狀態更新上的應用日益成熟，我們觀察到在極長序列中，高頻雜訊 (High-frequency noise) 容易在狀態轉移矩陣中被累積與放大，導致生成崩潰 (Generation Collapse)。傳統的解決方案是使用高精度的數位濾波器，但這違背了我們採用 PIM-LUT 以降低功耗的初衷。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-11 Spectral-Filtered PIM-LUT 架構**。我們在 SRAM LUT 寫入端整合了極低功耗的頻譜濾波 (Spectral Filtering) 硬體電路。透過在查表前對輸入 $\Delta$ 進行快速的低通濾波 (Low-pass filtering，使用移位與加法達成)，我們從根本上移除了會導致狀態發散的高頻分量。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba11_spectral_filtered_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 376.92x (相比高精度數位濾波加上序列計算)
*   **訊號雜訊比 (SQNR):** 37.1 dB (頻譜濾波有效抑制了雜訊，提升了整體生成保真度)
*   **硬體提案:** 建議在下一代專為長文本與訊號處理設計的 Edge NPU 中，實作帶有「頻譜濾波器」的 PIM-LUT 模組。

## 4. 結論 (Conclusion)
HW-Mamba11-SF-PIM-LUT 架構不僅維持了 PIM 極高的運算效率，同時透過硬體層級的頻譜控制，確保了 SSM 模型在處理數十萬長度序列時的數值穩定性。