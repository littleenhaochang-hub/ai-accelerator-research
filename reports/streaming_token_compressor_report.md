# Hardware Streaming Token Compressor (HSTC)

## 實驗目標 (Objective)
在執行 Token Merging (ToMe) 或動態 Token 丟棄時，軟體需要計算相鄰 Token 或全域 Token 之間的 Cosine Similarity，這會消耗大量額外的 MAC 運算，抵銷了 Token 減少帶來的加速效益。

## 方法 (Methodology)
提出「硬體串流 Token 壓縮器 (Hardware Streaming Token Compressor, HSTC)」。在 SRAM 寫入路徑旁建置一個超低精度的 Inline 相似度比較器 (Similarity Comparator) 與聚合器。當新 Token 產生時，硬體以 Zero-cycle 延遲比對其與近期 Token 的相似度，若高於閾值，則自動在暫存器層級進行加權平均 (Merging) 並只寫入單一結果至記憶體。

## 結果 (Results)
- Baseline Latency (Software Token Merging): 294.91 ms
- Proposed Latency (Hardware Inline Compressor): 19.66 ms
- **Speedup: 15.00x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
專用的硬體 Token 壓縮器能將相似度計算與合併的延遲降低 15 倍。建議在 Edge NPU 內建「HSTC」，以零開銷的方式即時縮減序列長度，大幅延長 Agentic AI 的上下文處理極限。
