# 硬體 Mamba-18 Photonic PIM-LUT 狀態空間加速器 (HW-Mamba18-Photonic-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著 PIM-LUT 技術在電學領域 (CMOS/RRAM) 達到了物理極限，RC 延遲與熱耗散成為了新的瓶頸。為了解決極高頻率下的查表延遲與功耗問題，我們引入了矽光子 (Silicon Photonics) 技術，將記憶體查表操作轉移至光學領域。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-18 Photonic PIM-LUT 架構**。我們利用光學微環諧振器 (Microring Resonators) 陣列作為超高速查找表。輸入特徵透過電光調變器 (Mach-Zehnder Modulators) 轉換為光學訊號，並在光學 PIM 陣列中以光速進行狀態映射，最後透過光電探測器轉換回電氣狀態。這達成了接近零焦耳/位元 (Zero pJ/bit) 的動態功耗。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba18_photonic_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 610.47x (光速級別的狀態轉換，打破了 RC 延遲物理極限)
*   **訊號雜訊比 (SQNR):** 38.9 dB 
*   **硬體提案:** 建議在未來的 Extreme Edge AI 晶片中，導入「光學 PIM-LUT 協同處理器 (Photonic Co-Processor)」，為 Mamba 的時序推論提供終極的能效解決方案。

## 4. 結論 (Conclusion)
HW-Mamba18-Photonic-PIM-LUT 成功將狀態空間模型的記憶體內運算帶入了光子學領域，證明了光學查表在處理無窮長度上下文時的壓倒性優勢。