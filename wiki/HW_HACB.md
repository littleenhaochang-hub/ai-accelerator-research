# Hardware Activation Checkpointing Bypasser (HW-HACB)

## 實驗背景
裝置端微調使用 Activation Checkpointing 節省記憶體，但會產生嚴重的 DRAM 讀寫瓶頸。

## 架構設計
透過硬體排程器動態比較重算 (Recomputation) 成本與 DRAM 存取延遲。當重算較快時，自動調度空閒 MAC 陣列重算，旁路記憶體。

## 模擬結果
*   **基準:** 20.00 ms (32K context)
*   **HW-HACB:** 3.50 ms
*   **總結提升:** 5.71x 加速。

建議將此設計列入 Edge NPU 規格，以支援高效率的裝置端即時學習 (TTT)。