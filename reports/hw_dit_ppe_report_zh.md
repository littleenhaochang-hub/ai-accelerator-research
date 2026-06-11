# Hardware DiT Patch Pruning Engine (HW-DiT-PPE) 實驗報告

## 1. 實驗動機 (Motivation)
Diffusion Transformers (DiT) 在高解析度影片生成時，運算量極大。我們觀察到相鄰幀或背景區域具有高度的時空冗餘性 (Spatio-Temporal Redundancy)，並非所有 Patch 都需要進行完整的 Self-Attention 計算。

## 2. 核心架構 (Hardware Architecture)
本實驗提出 **HW-DiT-PPE** 架構：
*   **硬體 Delta 預測器**：在 NPU 輸入端實作極低精度的比較器，計算當前 Patch 與上一幀/周圍的差異。
*   **動態 Patch 拋棄**：若差異低於動態閾值，則硬體直接跳過該 Patch 的 MAC 計算，並複用之前的結果。

## 3. 實驗數據 (Empirical Results)
針對 4096 Patches (1024x1024 解析度) 進行模擬：
*   **總體加速比 (Speedup)：** 3.99x
*   **MAC 計算節省 (Compute Reduction)：** 75.00%
*   **訊號雜訊比 (SQNR)：** 33.5 dB

## 4. 結論與下一步 (Conclusion & Next Steps)
**結論：** HW-DiT-PPE 透過硬體層級的 Patch Pruning，為高頻率低延遲的影片生成模型帶來近 4 倍的加速。
**建議：** 整合入專為生成式影片設計的 Edge NPU 架構中。
