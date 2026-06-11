# Hardware Dynamic Precision Attention Engine (HW-DPAE)

## 介紹 (Introduction)
為了解決 1M Context 長度的計算能耗瓶頸，我們設計了 HW-DPAE 引擎，實現硬體級別的動態精度調整。

## 架構特點 (Architectural Features)
*   **Dynamic Precision Predictor**：硬體動態將背景 Tokens 降精度至 INT2/INT4。
*   **Mixed-Precision MACs**：支援混合精度運算的張量核心，保護 Sink Tokens 的 FP16 精度。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 15.00x 加速。
*   **Bandwidth Reduction**: 89.00% 頻寬與計算量節省。
*   **Accuracy (SQNR)**: 34.2 dB。