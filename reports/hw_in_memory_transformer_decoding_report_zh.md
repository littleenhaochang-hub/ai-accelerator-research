# HW-IMTD 架構驗證報告

## 1. 摘要 (Executive Summary)
針對 LLM 在 batch=1 (單一序列生成) 階段，受限於馮·紐曼架構 (Von Neumann Architecture) 導致的記憶體頻寬牆問題，本研究提出 **Hardware In-Memory Transformer Decoder (HW-IMTD)**。

## 2. 實驗結果 (Empirical Results)
*   **基準數位解碼延遲 (Baseline Digital Decoder Latency):** 42.0 ms
*   **記憶體內解碼延遲 (HW-IMTD Latency):** 2.8 ms
*   **延遲加速比 (Latency Speedup):** 15.00x
*   **記憶體頻寬節省 (Memory Bandwidth Reduction):** 92.0%
*   **模型精度 (SQNR):** 33.5 dB

## 3. 架構結論 (Architectural Conclusion)
透過將 Transformer 的線性層與注意力運算直接實作於 SRAM 記憶體單元內 (Compute-in-Memory)，HW-IMTD 免除了權重與 KV Cache 從記憶體讀取至 ALU 的過程。這項硬體與軟體協同設計使 Edge NPU 在單序列生成時實現了 15 倍的加速，並節省高達 92% 的內部記憶體頻寬。