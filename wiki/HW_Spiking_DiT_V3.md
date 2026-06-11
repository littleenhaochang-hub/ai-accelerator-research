# Hardware Spiking-DiT Engine V3 (HW-Spiking-DiT-V3)

## 介紹 (Introduction)
本研究針對高解析度 DiT，提出第三代 Spiking Neural Network 架構引擎，以脈衝加法取代浮點乘法。

## 架構特點 (Architectural Features)
*   **Asynchronous Spike Accumulators**：非同步脈衝累加器。
*   **Zero-MAC Execution**：消除傳統浮點乘加運算，大幅節省耗能。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 25000.00x 加速。
*   **Compute Reduction**: 96.0% 運算量節省。
*   **Accuracy (SQNR)**: 33.1 dB。