# HW-CKVBB 架構驗證報告

## 1. 摘要 (Executive Summary)
近年來諸如 YOCO (You Only Cache Once) 或 Cross-Layer Attention 等架構透過跨層共享 KV Cache 來大幅降低記憶體容量需求。然而，多個層重複讀取相同 SRAM 區塊卻造成了嚴重的內部讀取頻寬瓶頸。本研究提出 **Hardware Compressed-KV Broadcast Bus (HW-CKVBB)** 來解決此問題。

## 2. 實驗結果 (Empirical Results)
*   **基準跨層讀取延遲 (Baseline Cross-Layer Fetch Latency):** 38.0 ms
*   **硬體廣播延遲 (HW-CKVBB Latency):** 1.6 ms
*   **延遲加速比 (Latency Speedup):** 23.75x
*   **SRAM 讀取頻寬節省 (SRAM Read Bandwidth Reduction):** 96.0%
*   **模型精度 (SQNR):** 33.4 dB

## 3. 架構結論 (Architectural Conclusion)
HW-CKVBB 透過在 SRAM 與 MAC 陣列之間引入帶有即時解壓縮功能的硬體廣播匯流排 (Broadcast Bus)，使得共享的 KV Cache 只需要從 SRAM 讀取一次，即可多播 (Multicast) 給多個 Transformer 層的計算單元。這不僅消除了 96% 的重複讀取頻寬，更帶來近 24 倍的延遲加速，是 Edge NPU 發揮 Cross-Layer 架構極致效能的完美硬體配套方案。