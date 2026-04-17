# Auto-Researcher 報告: 長文本 Prefill OOM 解決方案

## 摘要
在 Edge NPU 處理極長文本 (例如 32K tokens) 時，Prefill 階段的 $O(N^2)$ Attention Matrix 與完整的 KV Cache 往往會導致嚴重的 OOM (Out-of-Memory) 崩潰或迫使系統頻繁在 DRAM 與 SSD 之間進行 Swap。為解決長文本 Prefill OOM 的問題，我們結合了「Chained Householder Reflections 的 4-bit KV Cache 壓縮」與「Chunked Attention」。

## 實驗設定
- 序列長度 (Seq Len): 32000 tokens
- 模型維度: 4096 (32 Layers)
- Chunk Size: 4096 tokens

## 模擬結果
* **KV Cache Size:**
  * Baseline (FP16): 16000.00 MB
  * Proposed (4-bit Householder): 4000.00 MB (降低 75.00%)
* **Attention Matrix Memory (Prefill 峰值):**
  * Baseline ($O(N^2)$): 62500.00 MB
  * Proposed (Chunked): 8000.00 MB (降低 87.20%)

## 結論與架構建議
針對長文本，硬體上應實作基於 Chunk 處理的非同步 DMA 預取器，將超大序列切片計算。同時，我們強烈建議將 Chained Householder Reflections (壓縮 KV Cache 至 4-bit) 直接燒錄至 NPU 的 KV Cache Manager 中，使 Edge 裝置能在有限的 Unified Memory (<16GB) 中完整容納 32K 上下文而不發生 OOM。
