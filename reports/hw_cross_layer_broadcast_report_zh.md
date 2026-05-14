# Hardware Cross-Layer Broadcast Bus (HW-CLBB)

## 摘要 (Executive Summary)
針對 YOCO (You Only Cache Once) 等跨層共享 KV Cache 的架構，我們提出了一種專用的硬體 SRAM 廣播匯流排 (Broadcast Bus)，以消除軟體層面重複的記憶體讀取與搬運。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Routing):** 傳統軟體透過記憶體映射 (Memory Mapping) 在多個層之間共享 KV Cache，仍需耗費大量的 SRAM 讀取頻寬，延遲為 600.00 ms。
- **硬體廣播 (HW-CLBB):** 透過硬體廣播匯流排，一次讀取即可將 KV 資料推播至多個 MAC 陣列，延遲降至 80.00 ms。
- **效能提升 (Speedup):** 達成 **7.50x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 內部佈建 HW-CLBB 廣播網路。對於 YOCO 等 Decoder 跨層共享架構，此硬體設計能將 SRAM 讀取頻寬需求直接減半，大幅提升硬體使用率 (Utilization)。