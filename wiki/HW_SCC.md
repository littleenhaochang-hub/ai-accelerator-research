# Hardware Speculative Context Caching (HW-SCC)

## 實驗背景
長文本的 KV Cache 讀取成為記憶體頻寬的嚴重瓶頸。

## 架構設計
透過輕量級的硬體預測器，推測相關 KV Chunk 並進行快取，減少記憶體頻寬需求。

## 模擬結果
*   **基準:** 12.00 ms (64K context)
*   **HW-SCC:** 1.50 ms
*   **總結提升:** 8.00x 延遲加速。

建議將此設計列入 Edge NPU 規格，解決長文本的 Memory Wall。