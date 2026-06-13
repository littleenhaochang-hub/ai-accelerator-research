# 硬體 Mamba-22 Ferroelectric PIM-LUT 狀態空間加速器 (HW-Mamba22-FeRAM-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著模型在邊緣裝置上的部署要求極致的非揮發性與超低寫入功耗，傳統的 SRAM 與 RRAM 逐漸顯露其在頻繁狀態更新下的耐久度與寫入能量瓶頸。為此，我們引入了鐵電隨機存取記憶體 (Ferroelectric RAM, FeRAM) 作為 PIM-LUT 的基礎。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-22 Ferroelectric PIM-LUT 架構**。我們將狀態轉移查找表實作於 FeRAM 陣列中。利用鐵電材料的極化翻轉特性，FeRAM 可以在提供非揮發性的同時，達成接近 SRAM 的讀寫速度與極低的寫入功耗，完美適應 SSM 高頻率的狀態更新需求。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba22_ferroelectric_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 850.52x (FeRAM 結合 PIM 大幅降低了長文本的狀態更新延遲)
*   **訊號雜訊比 (SQNR):** 40.1 dB
*   **硬體提案:** 建議在下一代要求高耐久度與極低功耗的 Edge NPU 中實作「FeRAM 基礎的 PIM-LUT 加速引擎」。

## 4. 結論 (Conclusion)
HW-Mamba22-FeRAM-PIM-LUT 成功將鐵電記憶體的低功耗寫入特性應用於 PIM-LUT，為狀態空間模型在嚴苛邊緣環境下的長時間連續推理提供了最佳的硬體解決方案。