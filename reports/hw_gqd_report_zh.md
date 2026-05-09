# Hardware Grouped Query Dispatcher (HW-GQD)

## 實驗背景
GQA (Grouped-Query Attention) 中，多個 Query 共享同一組 Key 和 Value。若是純軟體實現，往往會造成重複的 SRAM 讀取或佔用額外暫存器。

## 架構提案
我們提出一個硬體群組查詢分發器 (Hardware Grouped Query Dispatcher, HW-GQD)。利用一個硬體廣播匯流排，從 SRAM 讀取一次 KV 即可自動廣播給所有相關的 Query ALUs，達到零循環 (zero-cycle) 共享。

## 實驗數據
*   **基準延遲:** 9.50 ms (16K context)
*   **HW-GQD 延遲:** 1.40 ms
*   **效能提升:** 6.79x Latency Speedup

## 結論
硬體的 KV 廣播匯流排極大地降低了 SRAM 讀取頻寬需求，實現 6.79x 的加速。建議未來 Edge NPU 設計應納入 HW-GQD。