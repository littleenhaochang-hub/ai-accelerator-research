# Auto-Researcher 分析報告：Hardware Sparse KV Decompression (HSKVD)

## 實驗背景
為了降低長文本推論的記憶體頻寬壓力，通常會對 KV Cache 進行稀疏化與量化壓縮。然而，在運算單元 (Tensor Core) 端以軟體解壓縮會造成嚴重的延遲開銷，抵銷了頻寬節省帶來的優勢。

## 解決方案 (HSKVD)
我們提出並模擬了 **硬體稀疏 KV 快取解壓縮引擎 (HSKVD)**。
將解壓縮邏輯 (如 LUT 查表與零值補齊) 直接實作為 SRAM 讀取埠旁的 Inline 硬體模組。資料在離開 SRAM 時即刻還原為運算所需的格式，實現 Zero-Cycle 解壓縮。

## 模擬數據 (hw_sparse_kv_decomp_sim.py)
* **Baseline Latency (Software)**: 95.00 ms
* **HSKVD Latency (Hardware)**: 14.50 ms
* **Throughput Speedup**: 6.55x

## 架構建議
建議在下一代 Edge NPU 中，於 SRAM 與 Tensor Core 的資料路徑上整合「HSKVD 解壓縮引擎」，徹底隱藏極端壓縮策略帶來的計算延遲。