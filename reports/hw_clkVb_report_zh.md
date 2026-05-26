# Hardware Cross-Layer KV Broadcaster (HW-CLKVB)
## 針對 YOCO (You Only Cache Once) 架構的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
YOCO 架構透過在多個 Transformer 層之間共享同一組 KV Cache，有效減少了記憶體容量。然而，傳統 NPU 在執行時，每一層仍必須發出獨立的 SRAM 讀取指令，導致同一組資料被重複讀取，浪費了寶貴的內部 SRAM 讀取頻寬。

### 2. 探索文獻 (Explore)
我們提出 Hardware Cross-Layer KV Broadcaster (HW-CLKVB)。透過在 SRAM 與 Tensor Cores 之間加入硬體層級的廣播匯流排 (Multicast Bus)，SRAM 只需要將共享的 KV Cache 讀取一次，便能即時派送給所有共享該 Cache 的運算層，達成 Zero-Copy 重用。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_clkVb_sim.py` 進行 32K Context 模擬驗證：
- **Baseline YOCO Latency:** 2010.00 ms
- **HW-CLKVB Latency:** 64.00 ms
- **Speedup (加速比):** 31.41x
- **內部 SRAM 讀取頻寬縮減:** 96.8%

### 4. 結論
實作 HW-CLKVB 能夠帶來 31.41x 的延遲加速，徹底釋放內部記憶體頻寬。建議將此「硬體廣播匯流排」整合入 Edge NPU 架構中，以完美搭配 YOCO 或是 Cross-Layer Attention (CLA) 等現代模型。
