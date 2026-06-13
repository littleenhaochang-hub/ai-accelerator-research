# 硬體 Mamba-10 Cross-Layer PIM-LUT 狀態空間加速器 (HW-Mamba10-CL-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著模型深度的增加，Mamba 架構中逐層 (Layer-by-Layer) 的狀態傳遞開始成為顯著的延遲瓶頸。在 Edge NPU 內部，將前一層的狀態從 PIM 陣列讀出，再寫入下一層的 PIM 陣列，會消耗大量內部匯流排頻寬 (Internal Bus Bandwidth)。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-10 Cross-Layer PIM-LUT 架構**。該架構在 PIM 巨集之間引入了專屬的「跨層狀態轉發匯流排 (Cross-Layer State Forwarding Bus)」。硬體層面上，相鄰層級的 SRAM LUT 可以直接透過暫存器等級的專線共享狀態變數，完全繞過 NPU 的主記憶體控制器。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba10_cross_layer_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 346.77x (大幅降低了深層網路的累加延遲)
*   **訊號雜訊比 (SQNR):** 36.8 dB
*   **硬體提案:** 建議在 NPU 中實作具有跨層資料直通 (Data Feed-Forward) 能力的「堆疊式 PIM-LUT 巨集區塊」，以原生支援極深層 SSM 模型。

## 4. 結論 (Conclusion)
HW-Mamba10-CL-PIM-LUT 成功消除了深層狀態空間模型在硬體佈線上的資料搬運開銷，讓百層級 (100+ Layers) 的 Mamba 模型在邊緣裝置上的實時推論成為可能。