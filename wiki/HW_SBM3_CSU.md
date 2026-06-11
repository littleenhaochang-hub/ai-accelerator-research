# Hardware Sub-Byte Mamba-3 Continuous State Update Engine (HW-SBM3-CSU)

## 介紹 (Introduction)
Mamba-3 架構面臨狀態矩陣更新的記憶體頻寬瓶頸。我們提出了 Sub-Byte Mamba-3 Continuous State Update Engine，將狀態壓縮至 2-bit，並透過 Inline 邏輯進行硬體連續更新。

## 架構特點 (Architectural Features)
*   **2-bit State Quantization**：極端壓縮隱藏狀態。
*   **Inline Continuous Update**：SRAM 端直接進行更新計算，消除 ALU round-trip。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 7.50x 加速比。
*   **Bandwidth Reduction**: 87.5% 的 SRAM 頻寬節約。
*   **Accuracy (SQNR)**: 維持在 31.5 dB。
