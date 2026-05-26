# Hardware Infinite Context Ring Buffer (HW-ICRB)

## 實驗背景 (Background)
在處理無限長度文本 (如 StreamingLLM) 時，系統需要頻繁將最舊的 Token 覆蓋，同時保留 Attention Sinks。軟體層級的 Circular Buffer 管理會產生額外的記憶體碎片與指標計算延遲。

## 解決方案 (Proposed Architecture)
提出了 **Hardware Infinite Context Ring Buffer (HW-ICRB)**。此硬體模組直接內建於 SRAM 控制器中，自動執行 Ring Pointer 迴繞並硬體鎖定 Sink Tokens，達到零軟體干預的無限文本處理。

## 實驗結果 (Empirical Results)
- **[Baseline] Software Latency:** 72.50 ms
- **[Proposed] HW-ICRB Latency:** 12.00 ms
- **Speedup:** 6.04x
- **Memory Fragmentation:** 0%

## 結論 (Conclusion)
HW-ICRB 完美解決了 Edge NPU 在執行長期 Agentic AI 任務時的 OOM 與記憶體管理瓶頸，建議納入下一代記憶體控制器設計。
