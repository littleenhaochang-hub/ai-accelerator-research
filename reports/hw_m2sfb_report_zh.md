# Hardware Mamba-2 State Forwarding Bus (HW-M2SFB) 實驗報告

## 背景與瓶頸分析
Mamba-2 及相關 State Space Models (SSM) 在處理 Chunked Prefill 時，需要將前一個 Chunk 的隱藏狀態 (Hidden State) 傳遞給下一個 Chunk。在傳統 NPU 架構中，這意味著每個 Chunk 計算完畢後，必須將狀態矩陣寫回 SRAM，下一個 Chunk 再從 SRAM 讀取。這種頻繁的 SRAM R/W 不僅增加延遲，還會與權重抓取 (Weight Fetching) 產生頻寬競爭。

## 解決方案：HW-M2SFB (硬體狀態轉發匯流排)
我們提出 **HW-M2SFB**，一種專為 SSM 設計的硬體層級轉發機制。透過在 Tensor Core 累加器與下一個運算單元之間建立「暫存器級別 (Register-level) 的轉發匯流排」，讓上一個 Chunk 的最終狀態直接流入下一個 Chunk 的初始暫存器，達到真正的零記憶體存取 (Zero-SRAM Access) 狀態傳遞。

## 實驗結果
透過 Python 模擬 (`hw_m2sfb_sim.py`)，針對 8K Context (分為 32 個 256-token Chunks) 進行測試：
- **基準延遲 (SRAM R/W):** 0.0800 ms
- **HW-M2SFB 延遲 (Register Forwarding):** 0.0032 ms
- **狀態傳遞加速比 (Speedup):** 25.00x

## 結論
HW-M2SFB 完全消除了 Mamba-2 模型在 Chunk 間傳遞狀態時的記憶體頻寬開銷。雖然這部分的絕對延遲不大，但其釋放的 SRAM 頻寬能有效避免運算單元因等待記憶體而產生的 Pipeline Bubble。強烈建議將此轉發匯流排整合至下一代原生支援 SSM 的 Edge NPU 架構中。
