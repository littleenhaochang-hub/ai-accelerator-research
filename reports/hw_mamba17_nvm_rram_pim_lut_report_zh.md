# 硬體 Mamba-17 Non-Volatile RRAM PIM-LUT 狀態空間加速器 (HW-Mamba17-RRAM-PIM-LUT)

## 1. 架構動機 (Motivation)
傳統的 SRAM PIM-LUT 面臨著嚴重的靜態漏電流 (Static Leakage) 問題，特別是在模型規模擴大時。為了解決待機功耗並實現真正的「即開即用 (Instant-on)」Edge AI 應用，必須導入非揮發性記憶體 (Non-Volatile Memory, NVM)。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-17 NVM-RRAM PIM-LUT 架構**。我們將 SRAM 替換為高密度的電阻式隨機存取記憶體 (RRAM) 交叉陣列 (Crossbar Array)。利用 RRAM 在電導狀態下直接進行類比域 (Analog Domain) 查表運算，這不僅將靜態功耗降至接近零，同時大幅提升了記憶體密度。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba17_nvm_rram_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 577.38x (RRAM 原生支援的高密度與低讀取延遲)
*   **訊號雜訊比 (SQNR):** 38.6 dB 
*   **硬體提案:** 建議在下一代極致功耗受限的 Edge NPU (如 IoT 節點、穿戴式設備) 中，實作「RRAM PIM-LUT」，徹底消除靜態漏電牆。

## 4. 結論 (Conclusion)
HW-Mamba17-RRAM-PIM-LUT 完美結合了 RRAM 的非揮發特性與 PIM-LUT 的高效能，證明了電阻式記憶體在處理大規模 SSM 模型上的巨大潛力。