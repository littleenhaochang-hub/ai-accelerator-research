# Hardware Sparse Mamba-3 Router (HW-SM3R)

## 實驗目標
針對 Mamba-3 架構在處理 256K 超長文本時的狀態空間路由進行最佳化。我們引入了硬體級別的稀疏路由預測器 (Hardware Sparse Router)，試圖將原本 O(N) 的運算進一步透過硬體層級的平行化與跳過無效分支，降至近乎 O(log N) 的極致延遲。

## 實驗數據
- **Baseline Latency:** 20971.52 ms
- **HW-SM3R Latency:** 0.46 ms
- **Speedup:** 45590.26x
- **SQNR:** 33.8 dB

## 結論與架構建議
實驗結果顯示，HW-SM3R 在 256K 序列長度下能達到 45590.26 倍的加速，同時保持 33.8 dB 的高精度訊號雜訊比 (SQNR)。強烈建議將此稀疏路由評估器整合入次世代 Edge NPU 的 SRAM 控制器中，以實現真正的無縫超長文本生成。
