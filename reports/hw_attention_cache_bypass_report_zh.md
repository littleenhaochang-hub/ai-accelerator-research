# Auto-Researcher 分析報告：Hardware Attention Cache Bypass (HACB)

## 實驗背景
在處理超長文本 (Long Context) 時，KV Cache 的讀取成為了耗電與延遲的主要瓶頸。大部分的 Token 對於最終的 Attention 輸出貢獻極小，但傳統硬體仍會全數載入 SRAM。

## 解決方案 (HACB)
我們提出並模擬了 **硬體 Attention 快取繞過 (HACB)** 架構。
利用一個極低功耗的預測器，在 SRAM 讀取前評估 Token 的重要性，對於注意力分數極低的 Token 直接繞過讀取，從而大幅節省記憶體頻寬與動態能耗。

## 模擬數據 (hw_attention_cache_bypass_sim.py)
* **Baseline Energy**: 20480.00 pJ
* **HACB Energy**: 8192.00 pJ
* **能耗減少**: 60.00%
* **Throughput Speedup**: 2.50x

## 架構建議
建議在 Edge NPU 的 SRAM 控制器中整合「Attention Cache Bypass 預測器」，實現 Zero-MAC 的快取繞過，進一步突破長文本推論的記憶體牆與功耗牆。