# Hardware DiT Patch Pruning Engine (HW-DiT-PPE)

## 介紹 (Introduction)
本研究針對 Diffusion Transformers (DiT) 的時空冗餘性，提出在硬體層級動態捨棄不重要的背景或靜態 Patch。

## 架構特點 (Architectural Features)
*   **Inline Delta Predictor**：硬體直接計算 Patch 變化率。
*   **Dynamic Patch Dropping**：跳過冗餘 Patch 的 MAC 計算。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 3.99x 加速。
*   **Compute Reduction**: 75.0% MAC 運算節省。
*   **Accuracy (SQNR)**: 33.5 dB。
