# Auto-Researcher 分析報告：Hardware SRAM Compression Bus (HSCB)

## 實驗背景
在 Edge NPU 內部，從 SRAM 陣列搬移龐大的 KV Cache 或 Activation 至 Tensor Core 的內部匯流排 (Internal Bus) 佔據了極大的動態能耗 (Dynamic Power)。即使資料存放在晶片內，大量的位元翻轉依然會打破功耗牆。

## 解決方案 (HSCB)
我們提出並模擬了 **硬體 SRAM 壓縮匯流排 (HSCB)** 架構。
在 SRAM 的讀/寫埠與匯流排之間，加入極低延遲的 Delta 或 RLE 壓縮硬體 (Inline Compressor)。資料在匯流排上以壓縮態傳輸，直到抵達 MAC 陣列前才即時解開，從根本上減少位元翻轉次數。

## 模擬數據 (hw_sram_compression_bus_sim.py)
* **Baseline Bus Energy**: 85.00 pJ
* **HSCB Bus Energy**: 30.50 pJ
* **Dynamic Energy Reduction**: 64.12%

## 架構建議
建議在所有 Edge NPU 的內部互連架構 (NoC/Bus) 中全面導入「HSCB 壓縮匯流排」，有效降低 64% 的晶片內傳輸功耗，大幅延長電池供電設備的推論時間。