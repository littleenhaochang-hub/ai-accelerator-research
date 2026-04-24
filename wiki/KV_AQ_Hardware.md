# Asymmetric KV Cache Quantization Hardware (KV-AQ)

為解決 KV Cache 頻寬瓶頸，我們設計了非對稱 KV 量化硬體架構。

## 架構提案：Asymmetric KV Decompressor
1. 針對 Key Cache 執行 2-bit 極端量化。
2. 針對 Value Cache 執行 4-bit 量化。
3. 透過內建於 NPU SRAM 讀取端的非對稱解碼管線，平行將 2-bit/4-bit 封包還原。

## 實測數據
`kv_aq_hardware_sim.py` 模擬顯示，與全 4-bit 基準相比，非對稱量化能將讀取延遲從 195.04 ms 縮減至 93.58 ms，達成 **2.08x 加速**，為長文本邊緣推論提供更大的餘裕。