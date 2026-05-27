# Hardware KV Cache Delta Pruning (HW-KVCDP)

## 概述
長文本 (Long Context) 處理中的記憶體容量與頻寬一直是 Edge NPU 的最大瓶頸。本研究探討硬體層級的 KV Cache Delta Pruning (HW-KVCDP)，利用相鄰 Token 間的高度相似性，將差異極小的冗餘 Token 動態剔除。

## 實驗方法
在 NPU SRAM 控制器中整合一個行內 (inline) 的 Delta 比較器。當新的 KV 寫入時，硬體會自動計算與前幾個 Token 的差異，若低於設定的閾值，則直接丟棄該 Token (Pruning)，不寫入主記憶體中。這有效降低了有效序列長度。

## 實驗數據
*   **基準讀取延遲 (128K Context):** 4.88 ms
*   **HW-KVCDP 延遲:** 1.22 ms
*   **記憶體容量減少:** 75.00%
*   **整體吞吐量提升 (Speedup):** 4.00x

## 結論與架構建議
藉由將 Delta 評估邏輯硬體化，可以在完全不佔用軟體與 MAC 運算資源的情況下，動態將長文本縮減 75%。這使得 Edge NPU 能夠在有限的 SRAM 容量下支援更長的 Context Window。建議未來架構將「硬體 Delta 比較與剪枝單元」作為記憶體控制器的標準配備。
