# BNN 1-bit MAC Hardware (XNOR-Net) 驗證報告
## 實驗結果
- **傳統 INT4 能量消耗**: 0.580 pJ
- **1-bit BNN 能量消耗**: 0.012 pJ
- **能量降低**: 97.93%
- **吞吐量加速**: 8.50x
- **結論**: 透過將傳統的乘加運算替換為純邏輯的 XNOR 與硬體 Popcount 樹，1-bit 量化 (BNN) 展現了極致的功耗優勢，能耗降低達 97.93%。強烈建議在超低功耗的 Extreme Edge NPU 實作專屬的 1-bit XNOR-MAC 陣列。
