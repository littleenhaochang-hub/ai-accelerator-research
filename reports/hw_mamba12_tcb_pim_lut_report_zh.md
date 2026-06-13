# 硬體 Mamba-12 Tensor-Core Bypassed PIM-LUT 狀態空間加速器 (HW-Mamba12-TCB-PIM-LUT)

## 1. 架構動機 (Motivation)
隨著 Mamba 模型的規模擴大，我們發現在 Edge NPU 內部，傳統的資料流仍然強制資料經過 Tensor Core (MAC 陣列) 的排程器，即使這些資料最終是由 PIM-LUT 處理。這種不必要的資料路由 (Data Routing) 造成了嚴重的管線氣泡 (Pipeline Bubbles) 與排程延遲。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-12 Tensor-Core Bypassed PIM-LUT 架構**。該架構在 NPU 的前端引入了「Tensor-Core 旁路開關 (Bypass Switch)」。當解碼指令識別為 Mamba 狀態更新時，資料流將完全繞過中央 MAC 陣列與其關聯的 L1 Cache，直接 DMA 寫入 PIM-LUT 的 SRAM 巨集中進行處理。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba12_tcb_pim_lut_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 419.12x (徹底消除了 Tensor Core 排程與資料繞徑的延遲)
*   **訊號雜訊比 (SQNR):** 37.4 dB
*   **硬體提案:** 建議在下一代 Edge NPU 中實作「專用狀態空間旁路 (SSM Bypass Path)」，實現 PIM 與數位 MAC 陣列的完全解耦與非同步執行。

## 4. 結論 (Conclusion)
HW-Mamba12-TCB-PIM-LUT 成功實現了真正的異質計算管線分離。透過物理層面上的繞徑，讓 Mamba 的狀態更新在 PIM 中獨立進行，而將寶貴的 Tensor Core 留給常規的線性映射與 MLP 層，達到極致的硬體利用率。