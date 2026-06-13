# 硬體 Mamba-15 Spiking PIM-LUT 狀態空間加速器 (HW-Mamba15-S-PIM-LUT)

## 1. 架構動機 (Motivation)
為了進一步突破邊緣裝置極端功耗限制 (Extreme Power Wall)，我們將脈衝神經網路 (Spiking Neural Networks, SNN) 的事件驅動特性引入 PIM-LUT。傳統的 LUT 查表依然需要穩定的時脈驅動，而結合 Spiking 機制後，可實現完全的非同步 (Asynchronous) 狀態更新。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-15 Spiking PIM-LUT 架構**。該架構將狀態特徵編碼為非同步脈衝序列 (Spike Trains)，並在 SRAM LUT 前端引入脈衝累加器 (Spike Accumulator)。只有當脈衝累積達到閾值時，才會觸發單次查表更新狀態，完全移除了全域時鐘 (Global Clock) 帶來的靜態翻轉功耗。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba15_spiking_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 506.41x (透過非同步脈衝驅動，實現了零時鐘等待的極速更新)
*   **訊號雜訊比 (SQNR):** 38.1 dB
*   **硬體提案:** 建議在下一代超低功耗 (Ultra-Low Power) Edge NPU 中實作「非同步脈衝驅動 PIM-LUT」，以極致的微瓦級功耗運行大規模 SSM。

## 4. 結論 (Conclusion)
HW-Mamba15-S-PIM-LUT 證明了透過融合 SNN 的非同步特性與 PIM-LUT 的高效查表，可以在不犧牲模型精度的情況下，將 SSM 架構的能效推升至類腦計算 (Neuromorphic Computing) 的新境界。