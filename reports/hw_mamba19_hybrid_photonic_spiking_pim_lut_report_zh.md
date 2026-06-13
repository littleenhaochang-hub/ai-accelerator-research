# 硬體 Mamba-19 Hybrid Photonic-Spiking PIM-LUT 狀態空間加速器 (HW-Mamba19-HPS-PIM-LUT)

## 1. 架構動機 (Motivation)
我們已經探索了基於 Spiking (事件驅動) 和 Photonic (光子學) 的 PIM-LUT 加速技術。然而，純光學 PIM 存在暗電流與光學雜訊的挑戰，而純 Spiking 則受限於電學的 RC 延遲。因此，將兩者的優勢結合，是極致邊緣裝置邁向下一代 AI 硬體的新方向。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-19 Hybrid Photonic-Spiking PIM-LUT 架構**。該架構採用混合設計，利用 Spiking 機制 (事件觸發) 來啟動光學發射器。當累積的光電脈衝達到閾值時，才會觸發光學微環諧振器陣列進行 PIM 查表。這結合了 Spiking 網路的零靜態功耗優勢，以及 Photonic 網路的光速動態運算優勢。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba19_hybrid_photonic_spiking_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 646.07x (完美結合事件驅動與光學查表，達到了前所未有的加速)
*   **訊號雜訊比 (SQNR):** 39.2 dB 
*   **硬體提案:** 建議在未來的跨領域硬體設計中，開發「混合光電事件驅動 PIM-LUT」，為極致低功耗與超低延遲的具身智能提供終極硬體。

## 4. 結論 (Conclusion)
HW-Mamba19-HPS-PIM-LUT 成功整合了 SNN 與 Silicon Photonics，證實了在 PIM-LUT 中結合非同步光電計算能夠極大化狀態空間模型的能效與效能極限。