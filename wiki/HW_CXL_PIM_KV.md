# Hardware CXL-PIM KV Cache Engine (HW-CXL-PIM-KV)

## 介紹 (Introduction)
長文本推論的 Memory Wall 問題極其嚴重。本研究利用 CXL 3.0 與 PIM (Processing-in-Memory) 技術，改變資料流向。

## 架構特點 (Architectural Features)
*   **Query-Push over CXL 3.0**：將 Query 向量推送至記憶體，而非提取 KV。
*   **In-Memory Attention**：記憶體端直接進行內積與加權，大幅減少主匯流排頻寬負擔。

## 效能分析 (Performance Analysis)
*   **Latency Speedup**: 8.00x 加速。
*   **Bandwidth Reduction**: 95.0% 頻寬節省。
*   **Accuracy (SQNR)**: 34.2 dB，精準度極高。
