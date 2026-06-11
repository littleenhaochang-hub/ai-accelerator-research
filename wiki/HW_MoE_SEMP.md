# Hardware MoE Sub-Expert Micro-Paging (HW-MoE-SEMP)

## 介紹 (Introduction)
MoE (Mixture of Experts) 模型在推論解碼時，常遇到 PCIe 頻寬牆的問題。傳統的記憶體提取必須以完整的 Block 提取整個專家模型，但單一 Token 實際活化的權重極少。本研究提出了硬體層級的子專家微頁面切換機制。

## 架構特點 (Architectural Features)
*   **CXL 3.0 介面支援**：利用 Byte-addressable 與精細化定址來替代粗粒度的 PCIe NVMe Block transfers。
*   **4KB Micro-Paging**：根據預測活化的路徑，僅透過記憶體總線抓取所需的 4KB 微小頁面，大幅降低讀取頻寬浪費。
*   **Inline Controller**：內建於 Edge NPU DMA Controller 的硬體映射表，達到零 CPU 介入。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 6.61x 加速比。
*   **Bandwidth Reduction**: 85.0% 的 CXL/PCIe 頻寬節約。
*   **Accuracy (SQNR)**: 保持在 35.2 dB (因不涉及資料量化破壞，僅改變傳輸粒度)。
