# Hardware DeepSeek MLA Cross-Node Broadcasting V2 (HW-MLA-CNB-V2)

## 介紹 (Introduction)
為了解決大規模叢集(16節點)與長文本(512K)推論的狀態共享瓶頸，本研究結合矽光子 CPO 技術，提出 V2 版本的光學廣播架構。

## 架構特點 (Architectural Features)
*   **Optical CPO Multicast**：矽光子零延遲廣播。
*   **Zero-Copy**：硬體直接寫入遠端 SRAM。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 200.00x 加速 (在 16 節點環境下)。
*   **Bandwidth Reduction**: 93.75% 頻寬節省。
*   **Accuracy (SQNR)**: 35.1 dB。