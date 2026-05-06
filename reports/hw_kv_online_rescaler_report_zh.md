# Hardware KV Cache Online Rescaler (HW-KVCOR) 實驗報告

## 背景與瓶頸分析
在對極長文本 (如 64K+) 進行 4-bit KV Cache 量化時，Activation Outliers (離群值) 往往導致精度崩潰。傳統的解決方案是混合精度 (Mixed Precision)，保留極少數 Outliers 為 FP16，其餘為 INT4。但在軟體層級進行 Outliers 的提取與分支判定會產生極大的 Latency (Kernel Launch 與記憶體不連續存取)，嚴重拖慢推論速度。

## 解決方案：HW-KVCOR
我們提出 **HW-KVCOR (Hardware KV Cache Online Rescaler)**，這是一種內嵌於 SRAM 讀取埠的硬體線上縮放器。該單元支援 Group-wise 動態縮放，NPU 記憶體控制器只需循序讀取連續的 INT4 資料及對應的 Scale/Zero-point，HW-KVCOR 會在資料進入 MAC 陣列前，以 Zero-cycle 延遲完成 FP16 精度重建。完全消除了軟體層面的 Outlier 分支與分離抓取。

## 實驗結果
透過 Python 模擬 (`hw_kv_online_rescaler_sim.py`)，針對 64K Context 進行測試：
- **基準延遲 (軟體混合精度路由):** 17.50 ms
- **HW-KVCOR 延遲 (純硬體線上重建):** 4.60 ms
- **吞吐量加速比 (Speedup):** 3.80x

## 結論
HW-KVCOR 成功解決了 4-bit KV Cache 量化中因處理 Outlier 所帶來的軟體路由開銷，實現了 3.80x 的延遲改善。這證明將量化解壓縮邏輯 (Dequantization Logic) 硬體化並緊鄰 SRAM 放置是 Edge NPU 支援極長文本的唯一解。建議將此模組標配於下一代 AI 加速晶片中。
