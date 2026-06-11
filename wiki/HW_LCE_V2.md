# Hardware Local Context Extractor V2 (HW-LCE-V2)

## 介紹 (Introduction)
本研究提出硬體級別的 Local Context Extractor，動態濾除 98% 不相關的長文本資訊。

## 架構特點 (Architectural Features)
*   **INT2 Similarity Predictor**：硬體預測器。
*   **Zero-MAC Bypassing**：大幅節省記憶體讀取與 MAC 運算。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 32.14x 加速。
*   **Bandwidth Reduction**: 98.0% 記憶體與運算節省。
*   **Accuracy (SQNR)**: 32.5 dB。
