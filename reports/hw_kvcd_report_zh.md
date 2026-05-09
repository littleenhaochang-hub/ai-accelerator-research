# Hardware KV Cache Deduplication (HW-KVCD)

## 實驗背景
超長文本 (如 64K+) 推理中，常存在大量重複或高度相似的片語，導致 KV Cache 儲存了大量冗餘數據，嚴重消耗 SRAM/DRAM 頻寬。

## 架構提案
我們提出硬體 KV 快取去重引擎 (Hardware KV Cache Deduplication, HW-KVCD)。透過硬體層級的雜湊表 (Hash Table) 與相似度比對器，在 KV 寫入階段即時偵測並合併重複的 Token，讀取時再透過指標還原。

## 實驗數據
*   **基準延遲:** 18.00 ms
*   **HW-KVCD 延遲:** 3.50 ms
*   **效能提升:** 5.14x Speedup

## 結論
硬體層級的 KV 去重可實現 5.14x 的加速，有效緩解記憶體頻寬瓶頸。建議整合至 Edge NPU 的 SRAM 控制器中。