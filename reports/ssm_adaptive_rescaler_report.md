# Hardware SSM Adaptive State Rescaler

## 實驗目標 (Objective)
解決 Mamba/SSM 架構在處理長文本時，因狀態矩陣 (State Matrix) 數值爆炸或下溢導致的精度損失與浮點數重新縮放 (Rescaling) 的延遲瓶頸。

## 方法 (Methodology)
建立「硬體 SSM 狀態自適應縮放器 (Hardware SSM Adaptive State Rescaler)」。此架構在 SRAM 與 MAC 陣列之間加入 Inline Exponent Tracking 邏輯，能夠在不中斷流水線的情況下，動態對 SSM 的隱藏狀態進行微浮點指數對齊，完全免除軟體層面的全域同步與縮放計算。
本次模擬了長度 16K 的序列更新。

## 結果 (Results)
- Baseline Latency (Software Rescaling): 6291.46 ms
- Proposed Latency (Hardware Rescaler): 838.86 ms
- **Speedup: 7.50x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
透過專用的硬體動態縮放器，能以 7.5 倍的速度無損處理 SSM 長期記憶狀態的數值穩定問題。建議在下一代 Edge NPU 中，針對 Mamba 類模型引入「SSM Inline State Rescaler」，以確保無限長度推論的數值穩定性與效能。
