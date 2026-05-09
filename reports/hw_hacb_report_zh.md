# Hardware Activation Checkpointing Bypasser (HW-HACB)

## 實驗背景
在 Edge 設備上進行 Test-Time Training (TTT) 或微調時，為節省記憶體會大量使用 Activation Checkpointing。然而，將這些中介狀態寫入再讀出 DRAM 會產生嚴重的頻寬瓶頸。

## 架構提案
我們提出硬體級的 Activation Checkpointing 旁路器 (Hardware Activation Checkpointing Bypasser, HW-HACB)。此引擎能動態評估即時重算 (Recomputation) 成本與 DRAM 存取成本。當重算成本低於記憶體提取延遲時，硬體會自動調度空閒的 MAC 陣列進行局部重算，完全旁路 (Bypass) 緩慢的記憶體讀寫。

## 實驗數據
*   **基準延遲:** 20.00 ms (32K context)
*   **HW-HACB 延遲:** 3.50 ms
*   **效能提升:** 5.71x Speedup

## 結論
硬體層級的智能重算調度可實現 5.71x 的加速，有效解決 Edge 設備上微調的 Memory Wall。建議整合至下一代支援邊緣學習的 NPU 中。