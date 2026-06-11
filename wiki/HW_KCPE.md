# Hardware K-Cache Pruning Engine (HW-KCPE)

## 介紹 (Introduction)
長文本解碼的 Memory Wall 主要來自 KV Cache。HW-KCPE 透過硬體預測，直接跳過不必要的 K-Cache 讀取。

## 架構特點 (Architectural Features)
*   **Inline K-Cache Predictor**：內建於記憶體控制器。
*   **DRAM Burst Canceling**：硬體直接取消無效的 DRAM 讀取請求。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 5.38x 加速。
*   **Bandwidth Reduction**: 85.0% 記憶體頻寬節省。
*   **Accuracy (SQNR)**: 32.7 dB。
