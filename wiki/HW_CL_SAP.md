# Hardware Cross-Layer Sparse Attention Predictor (HW-CL-SAP)

## 介紹 (Introduction)
本研究探討如何利用 Transformer 層與層之間的注意力分數相似度，在硬體層面實現動態稀疏計算。

## 架構特點 (Architectural Features)
*   **Cross-Layer Sparsity Prediction**：硬體快取前一層的稀疏特徵，直接映射至當前層。
*   **Inline MAC Bypassing**：硬體層級跳過無效的 MAC 計算。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 5.14x 加速。
*   **Compute Reduction**: 80.0% 計算節省。
*   **Accuracy (SQNR)**: 32.8 dB。
