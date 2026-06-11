# Hardware 2-bit DeepSeek MLA Engine (HW-2B-MLA)

## 介紹 (Introduction)
本研究針對 DeepSeek MLA 架構，提出將 Latent Vector 進行 2-bit 極端量化的硬體架構，進一步突破 SRAM 讀取瓶頸。

## 架構特點 (Architectural Features)
*   **2-bit Latent Quantization**：大幅減少 SRAM 儲存與讀取量。
*   **Inline Decompression & Up-Projection**：硬體直接解壓縮並展開向量。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 6.82x 加速。
*   **Bandwidth Reduction**: 87.5% SRAM 頻寬節省。
*   **Accuracy (SQNR)**: 31.8 dB。
