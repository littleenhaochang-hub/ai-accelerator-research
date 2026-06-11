# Hardware SRAM Memory Coalescer (HW-SRAM-MC)

## 介紹 (Introduction)
為了解決 Sparse Attention 帶來的 SRAM 讀取碎片化問題，本研究提出了 HW-SRAM-MC，將離散的記憶體存取動態打包為連續資料流。

## 架構特點 (Architectural Features)
*   **Dynamic Coalescing Engine**：硬體層級的聚合器，將非連續的 Token 資料整併。
*   **Zero-Software Overhead**：消除軟體 Gather/Scatter 的巨大延遲。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 6.25x 加速。
*   **Bandwidth Utilization Improvement**: 大幅減少 84.0% 的無效匯流排佔用。
*   **Accuracy (SQNR)**: 33.6 dB。
