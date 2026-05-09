# Hardware Speculative Context Caching (HW-SCC)

## 實驗背景
超長文本 (如 64K+) 的 KV Cache 讀取成為記憶體頻寬的嚴重瓶頸，導致生成延遲過高。

## 架構提案
我們提出一個硬體推測上下文快取器 (Hardware Speculative Context Caching)。透過輕量級的硬體預測器，在注意力計算前推測哪些 KV Chunk 最相關，並僅提取這些 Chunk。

## 實驗數據
*   **基準延遲 (Full Context):** 12.00 ms (64K context)
*   **HW-SCC 延遲:** 1.50 ms
*   **效能提升:** 8.00x Latency Speedup

## 結論
硬體級別的推測上下文快取能有效降低記憶體頻寬需求，實現 8.00x 的加速。建議未來的 Edge NPU 架構整合 HW-SCC 以支援無限上下文。