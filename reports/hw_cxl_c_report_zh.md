# Hardware CXL-Attached Cache Manager (HW-CXL-C)
## 針對超長文本推論的 Disaggregated Memory 硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
在 256K 甚至 1M Token 的超長文本場景中，Edge NPU 內建 SRAM 與外部 LPDDR 皆無法容納數十 GB 的 KV Cache。目前常見解法是將過冷的 KV Cache 分頁交換 (Swap) 至 NVMe SSD。然而 NVMe 走的是 Block I/O，讀寫速度極慢 (約 7 GB/s)，並帶有極高的作業系統中斷與驅動程式延遲。

### 2. 探索文獻 (Explore)
我們提出 Hardware CXL-Attached Cache Manager (HW-CXL-C)。利用 Compute Express Link (CXL) 3.0 的 Memory-Semantic (Mem.io) 協定，NPU 可以將外部 CXL 記憶體擴展模組直接視為本地記憶體的延伸，實現 Byte-addressable 的存取，徹底繞過 Block I/O 儲存堆疊。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_cxl_c_sim.py` 進行 256K Context 模擬驗證：
- **Baseline NVMe Swap Latency:** 585147.86 ms
- **HW-CXL-C Latency:** 64001.00 ms
- **Speedup (加速比):** 9.14x

### 4. 結論
實作 HW-CXL-C 能帶來 9.14x 的長文本 Swap 加速比。建議未來針對高階 Edge AI Server 設計時，拋棄 NVMe Swapping 架構，全面整合「CXL 3.0 硬體快取管理器」以達成 Disaggregated Memory 架構的潛力。
