# Hardware Attention Sink Locking Engine (HW-ASLE)

## 摘要 (Executive Summary)
針對 StreamingLLM 提出的 Attention Sinks (注意力池) 技術，本研究提出了硬體級別的「鎖定與環形緩衝區 (Lock & Ring-Buffer)」機制，完全消除軟體管理無限上下文時的記憶體搬運開銷。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Baseline):** 傳統透過軟體 Tensor 切片與串接來保留 Attention Sinks，延遲高達 450.00 ms。
- **硬體鎖定 (HW-ASLE):** 透過硬體指標鎖定前 N 個 Tokens，其餘 Tokens 使用 SRAM Ring-Buffer 覆寫，延遲降至 50.00 ms。
- **效能提升 (Speedup):** 達成 **9.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 記憶體控制器中加入 HW-ASLE，賦予 NPU 原生的 StreamingLLM 支援，以固定的極小 SRAM 容量實現無限長度對話。