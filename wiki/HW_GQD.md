# Hardware Grouped Query Dispatcher (HW-GQD)

## 實驗背景
GQA (Grouped-Query Attention) 的軟體實作會有重複讀取 SRAM 或佔用過多暫存器的問題。

## 架構設計
透過在 SRAM 與 Tensor Core 之間加入硬體廣播匯流排，一次讀取 KV 就能分發給同一組的所有 Query ALUs。

## 模擬結果
*   **基準:** 9.50 ms (16K context)
*   **HW-GQD:** 1.40 ms
*   **總結提升:** 6.79x 延遲加速。

建議將此設計列入支援 GQA 的 Edge NPU 規格，節省 SRAM 讀取頻寬。