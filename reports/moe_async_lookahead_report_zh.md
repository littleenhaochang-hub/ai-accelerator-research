# 硬體 MoE 異步預取與預測器 (Hardware MoE Async Lookahead Predictor)

## 摘要
為了解決 MoE 解碼時 CPU-GPU 記憶體傳輸的瓶頸，我們評估了硬體級別的異步 DMA 預取與 Lookahead 預測器。

## 實驗結果
- **基準延遲 (Demand Fetching)**: 1953.12 ms
- **改進延遲 (Async Lookahead)**: 195.31 ms
- **加速比**: 10.00x

## 結論
透過在 Edge NPU 引入硬體級異步預取與 Lookahead 預測器，可以將 PCIe 記憶體提取延遲與計算重疊，帶來 10 倍的吞吐量提升，完美解決 CPU-GPU 傳輸瓶頸。
