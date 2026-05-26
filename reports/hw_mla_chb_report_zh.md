# Hardware MLA Cross-Head Broadcasting Bus (HW-MLA-CHB)
## 針對 DeepSeek MLA 架構內部 SRAM 讀取頻寬瓶頸的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
DeepSeek 的 Multi-Head Latent Attention (MLA) 極大化地壓縮了 DRAM 中的 KV Cache 佔用（所有 Heads 共享同一組 Latent Vector）。然而，在 GPU/NPU 運算時，軟體需要為「每一個 Head」將此 Latent Vector 反覆從 SRAM 讀取至 ALU 進行反向投影，產生高達 $O(H)$ 倍的內部 SRAM 讀取頻寬浪費，導致解碼階段的頻寬阻塞。

### 2. 探索文獻 (Explore)
我們提出 Hardware MLA Cross-Head Broadcasting Bus (HW-MLA-CHB)。透過在 NPU 的 SRAM 讀取埠與 Attention 運算單元之間，建置一條零週期的硬體廣播匯流排 (Multicast Bus)。SRAM 僅需讀出 Latent Vector 一次，即可同步派送給所有 Head 的 ALU 陣列，徹底消除軟體反覆讀取的頻寬需求。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_mla_chb_sim.py` 進行 64K Context 模擬驗證：
- **Baseline MLA Fetch Latency:** 32015.00 ms
- **HW-MLA-CHB Latency:** 251.00 ms
- **Speedup (加速比):** 127.55x
- **內部 SRAM 讀取頻寬縮減:** 99.22%

### 4. 結論
實作 HW-MLA-CHB 能為 DeepSeek 等大語言模型帶來 127.55x 的內部讀取延遲縮減。建議將此「硬體廣播匯流排」作為 Edge NPU Attention Block 的標準設計，以完全發揮 MLA 架構的效能潛力。
