# Hardware Dynamic MoE Token-Drop Router (HW-DMTDR)

## 介紹 (Introduction)
MoE 模型推論時，並非每個 Token 都需要龐大的專家參數。HW-DMTDR 利用硬體電路直接評估信心分數，跳過簡單 Token 的專家提取。

## 架構特點 (Architectural Features)
*   **Inline Confidence Checker**：硬體直接檢查 Routing Score。
*   **Dynamic Bypassing**：若低於閾值，則不提取大專家，大幅減少頻寬。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 1.53x 加速。
*   **Reduction**: 40.0% 記憶體與運算節省。
*   **Accuracy (SQNR)**: 33.1 dB。
