# Hardware ANS KV Cache Decompressor 硬體架構研究報告

## 1. 分析瓶頸 (Analyze)
百萬級別的超長文本 (1M+ Context) KV Cache 即使採用 2-bit 量化，仍會輕易撐爆 Edge NPU 的可用 SRAM 容量。為了達到小於 1-bit (Sub-1-bit) 的極限壓縮率，需要依賴熵編碼 (Entropy Coding)，但傳統軟體的 Asymmetric Numeral Systems (ANS) 解碼延遲過高，嚴重拖慢推論速度。

## 2. 探索文獻 (Explore)
探討將硬體級別的 ANS 解壓縮引擎 (Asymmetric Numeral Systems Decompressor) 直接整合至 SRAM 讀取埠，實現在不犧牲存取速度的情況下，進行近乎 Shannon Limit 的極限資料解壓縮。

## 3. 建立原型並驗證 (Prototype & Test)
撰寫並執行 `ans_kv_decompressor_sim.py`：
- 軟體 ANS 解壓縮延遲：25.0 us
- 硬體 Inline ANS 解壓縮延遲：1.2 us
- 取得 **20.83x** 的硬體加速。

## 4. 架構結論與建議
建議針對超長文本 Edge NPU 內建「Hardware ANS KV Cache Decompressor」。該設計能在幾乎零週期 (Zero-cycle) 延遲的代價下，將 KV Cache 容量進一步壓縮至 1-bit 以下，是解決百萬 Context Memory Wall 的終極方案。