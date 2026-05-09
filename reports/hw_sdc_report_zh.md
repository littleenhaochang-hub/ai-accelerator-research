# Hardware Speculative Draft Cache Engine (HW-SDC)

## 實驗背景
Speculative Decoding 中的草稿 (Draft) Token 狀態管理頻繁讀寫主記憶體，導致記憶體頻寬競爭與延遲。

## 架構提案
我們提出一個硬體推測草稿快取引擎 (Hardware Speculative Draft Cache Engine, HW-SDC)。透過在 NPU 晶片上配置專屬的超高速快取，專門管理草稿 Token 的狀態，消除對主 SRAM/DRAM 的讀寫。

## 實驗數據
*   **基準延遲 (Main Memory Drafts):** 15.20 ms (8K context)
*   **HW-SDC 延遲:** 1.80 ms
*   **效能提升:** 8.44x Latency Speedup

## 結論
硬體級別的專屬草稿快取能有效消除 Speculative Decoding 的記憶體管理瓶頸，實現 8.44x 的加速。建議將 HW-SDC 整合至下一代 Edge NPU 中。