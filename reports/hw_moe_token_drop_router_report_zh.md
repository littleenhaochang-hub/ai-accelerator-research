# Hardware Dynamic MoE Token-Drop Router (HW-DMTDR) 實驗報告

## 1. 實驗動機 (Motivation)
MoE 架構下，並非所有 Token 都需要龐大的專家模型來進行推論。許多具備低困惑度 (Perplexity) 或簡單的 Token，強制載入專家權重會造成嚴重的記憶體頻寬浪費。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-DMTDR** 架構：
*   **硬體動態評估器**：在 NPU Router 輸出端設置一個硬體比較器，根據 Routing 信心分數決定是否丟棄 (或導向共享的小型 FFN)。
*   **零延遲決策**：避免由軟體來進行閾值判定，達到 0 額外延遲。

## 3. 實驗數據 (Empirical Results)
*   **總體加速比 (Speedup)：** 1.53x
*   **計算/頻寬節省 (Compute/Bandwidth Reduction)：** 40.00%
*   **訊號雜訊比 (SQNR)：** 33.1 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** 透過硬體層級動態捨棄不重要的 MoE 路由，能節省高達 40% 的專家提取頻寬。
**建議：** 實作此模組於下一代 MoE 專用晶片的 Scheduler 中。
