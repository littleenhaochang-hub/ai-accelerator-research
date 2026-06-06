# 硬體 MoE 空間多工專家預取器 (HW-MoE-SMEP)

## 摘要
在邊緣設備上執行 Mixture of Experts (MoE) 架構時，最嚴重的瓶頸來自於 CPU-GPU 之間的記憶體傳輸延遲（特別是從 Flash/NVMe 讀取專家權重）。為了打破這個「記憶體牆」，我們探討了將 MoE 專家提取機制從單一串流、阻塞式的 PCIe 讀取，遷移至硬體層級的**空間多工專家預取器 (Spatially-Multiplexed Expert Prefetcher, SMEP)**。

## 實驗設計
*   **基準模型 (Baseline):** 傳統的按需加載 (Demand Fetching)，每當路由網路選定專家時，才透過 PCIe Gen4 x8 進行阻塞式讀取。
*   **硬體架構 (HW-MoE-SMEP):** 整合了具備 85% 準確率的硬體路由預測器，並透過多通道 (Multi-Channel) DMA 並行讀取 Flash/NVMe 儲存空間。預測成功的專家權重將在計算前異步載入 SRAM，將存取延遲隱藏於計算之中。
*   **參數設定:** 4096 Tokens, 128 Experts, 專家大小 100MB, 帶寬 16 GB/s。

## 實驗結果
*   **基準延遲:** 25000.00 ms
*   **SMEP 延遲:** 3800.59 ms
*   **吞吐量加速:** **6.58 倍**

## 架構結論
傳統基於軟體中斷的 MoE 專家加載在邊緣設備上完全不可行。我們的實驗證明，透過將路由預測與多通道 DMA 預取邏輯燒錄進硬體 (HW-MoE-SMEP) 中，可以消除高達 85% 的 PCIe 延遲，達到 6.58 倍的加速。我們建議未來的 Edge NPU 在 DMA 控制器旁直接封裝 SMEP 模組，以支援超大規模的 MoE 推理。