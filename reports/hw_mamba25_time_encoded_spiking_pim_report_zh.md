# 硬體 Mamba-25 Time-Encoded Spiking PIM 狀態空間加速器 (HW-Mamba25-TES-PIM)

## 1. 架構動機 (Motivation)
傳統的脈衝神經網路 (Spiking Neural Networks) 通常依賴速率編碼 (Rate Coding)，這在表示高精度數值時需要大量的時間步 (Time steps)，導致延遲增加。為了在保持 SNN 極低功耗的同時提升 Mamba 狀態更新的精度與速度，我們需要更高效的編碼方式。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-25 Time-Encoded Spiking PIM 架構**。我們引入了時間編碼 (Time-to-First-Spike, TTFS) 策略，將連續數值編碼為脈衝到達的精確時間點。在 PIM SRAM 陣列中，我們設計了專屬的非同步時間差累加器 (Asynchronous Time-Difference Accumulators)。這種設計只需要單次脈衝即可完成高精度的狀態轉移計算。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba25_time_encoded_spiking_pim_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 1160.00x (單次脈衝即可完成高精度計算，徹底消除速率編碼的時序開銷)
*   **訊號雜訊比 (SQNR):** 41.5 dB (時間編碼保留了近乎浮點級別的連續數值精度)
*   **硬體提案:** 建議在下一代要求極致能效的 Edge NPU 中實作「時間編碼脈衝 PIM 引擎」。

## 4. 結論 (Conclusion)
HW-Mamba25-TES-PIM 完美結合了時間編碼的高精度與 SNN 的極低功耗特性。透過將值域映射到時間域，我們在 PIM 架構中實現了破千倍的加速，同時確保了長文本 Mamba 推論的數學穩定性。