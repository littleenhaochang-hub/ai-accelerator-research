# Hardware In-SRAM Sparse Predictor V2 (HW-IS-SP-V2)

## 實驗目標
探討在 SRAM 內部 (Processing-in-Memory) 直接進行高稀疏度矩陣預測的效益。當模型具有高達 90% 的稀疏性時，透過 SRAM 內部的位元線邏輯，直接跳過對應的 MAC 運算，避免將無效的零值傳輸至 Tensor Cores。

## 實驗數據
- **Baseline Latency:** 6553.60 ms
- **HW-IS-SP-V2 Latency:** 655.46 ms
- **Speedup:** 10.00x
- **SQNR:** 33.6 dB

## 結論與架構建議
實驗證明，HW-IS-SP-V2 能在 128K 序列與 90% 稀疏度的情境下，達成完美的 10 倍加速，幾乎等同於移除了所有無效運算的開銷。強烈建議在未來 Edge NPU 的 SRAM 陣列中整合此 PIM 稀疏預測器。
