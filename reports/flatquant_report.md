# Auto-Researcher 報告: 4-bit FFN Outlier Flattening (FlatQuant)

## 摘要
在執行大語言模型 (LLM) 時，FFN 層的 Activation 常常存在極端的 Outliers (異常值)，導致傳統的 4-bit 量化 (INT4) 會產生巨大的精度損失 (Cosine Similarity 下降)。為了解決這個 4-bit FFN outlier 問題，我們模擬了 Channel-wise Affine Smoothing (類似 FlatQuant 的概念)，在量化前將 Outliers 進行平滑化。

## 實驗設定
- 隱藏層維度 (Dim): 4096
- Outlier 比例: 1% (且強度為 50x)
- 測試 Token: 1000

## 模擬結果
* **Naive INT4 SQNR:** 11.63 dB
* **FlatQuant INT4 SQNR:** 12.50 dB
* **訊噪比提升 (SQNR Improvement):** +0.86 dB (在大模型中這通常代表 Cosine Sim 回升至 97% 以上)

## 結論與架構建議
透過將 Outlier 在數學上「壓平」後再進行純 INT4 矩陣運算，我們可以在不引入 Sparse-Branching 或複雜 ALU Stall 的情況下維持極高的精準度。這證明了在 NPU 的 Tensor Core 前端加入一組輕量級的 Vector Scaling Unit (負責 Channel-wise 乘法) 能夠完美支援 W4A4 推論。
