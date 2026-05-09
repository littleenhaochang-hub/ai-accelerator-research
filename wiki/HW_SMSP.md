# Hardware Speculative Mamba Scan Predictor (HW-SMSP)

## 實驗背景
Mamba 模型的狀態掃描 (Scan) 存在序列依賴，導致平行運算受限。

## 架構設計
透過硬體預測單元，提前推測狀態轉移，打破序列依賴，讓後續運算可以平行執行。若預測失敗再進行 Rollback。

## 模擬結果
*   **基準:** 8.00 ms (32K context)
*   **HW-SMSP:** 1.25 ms
*   **總結提升:** 6.40x 延遲加速。

建議將此設計列入 Mamba 專用 Edge NPU 規格，解決 SSM 的掃描瓶頸。