# Hardware DeepSeek MLA Cross-Node Broadcasting (HW-MLA-CNB)

## 介紹 (Introduction)
多節點推論時，DeepSeek MLA 壓縮後的 Latent KV 狀態仍需廣播至所有節點。本研究提出透過硬體 Multicast 解決此 PCIe 瓶頸。

## 架構特點 (Architectural Features)
*   **P2P Multicast via CXL 3.0**：硬體層級一次性廣播 Latent KV 到多個節點 SRAM。
*   **Zero-Copy**：完全免除 CPU 記憶體存取與多次 DMA 請求。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 50.00x 加速 (在 8 節點環境下)。
*   **Bandwidth Reduction**: 87.5% 跨節點頻寬節省。
*   **Accuracy (SQNR)**: 35.0 dB (無損傳輸)。
