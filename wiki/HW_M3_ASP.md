# Hardware Mamba-3 Associative Scan PIM Engine (HW-M3-ASP)

## 介紹 (Introduction)
本研究探討將 Mamba-3 的平行關聯掃描 (Associative Scan) 邏輯移至 Processing-in-Memory (PIM) 內執行，以突破超長文本 (512K) 的記憶體頻寬瓶頸。

## 架構特點 (Architectural Features)
*   **PIM-based Scan Tree**：在 SRAM 內部建構硬體樹狀掃描網路。
*   **O(log N) Latency**：將 O(N) 軟體迴圈轉化為對數級硬體延遲。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 66225.85x 加速。
*   **Bandwidth Reduction**: 98.0% 主匯流排頻寬節省。
*   **Accuracy (SQNR)**: 34.6 dB。
