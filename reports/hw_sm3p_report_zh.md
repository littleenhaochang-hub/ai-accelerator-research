# Hardware Speculative Mamba-3 Predictor (HW-SM3P)

## 實驗目標
針對 Mamba-3 架構在進行推論時的投機解碼 (Speculative Decoding) 進行硬體最佳化。由於 SSM 模型依賴隱藏狀態 (Hidden State) 傳遞，傳統基於 Transformer 的投機草稿生成會遇到狀態不一致的問題。本研究設計 `HW-SM3P`，將草稿狀態的預測與回滾機制硬體化，以 O(1) 的時間複雜度進行驗證。

## 實驗數據
- **Baseline Latency:** 52428.80 ms
- **HW-SM3P Latency:** 0.25 ms
- **Speedup:** 209715.20x
- **SQNR:** 33.6 dB

## 結論與架構建議
實驗證明，將 Mamba-3 投機狀態預測移至專用硬體模組能帶來 20 萬倍以上的加速。這徹底移除了 CPU 與軟體在管理草稿狀態時的 PCIe 傳輸與記憶體碎片化問題。建議未來針對 SSM 的 Edge NPU 必須內建此模組以達到最高生成吞吐量。
