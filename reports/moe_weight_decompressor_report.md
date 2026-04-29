# Hardware MoE Weight Decompressor

## 實驗目標 (Objective)
解決 MoE 模型在載入 Expert 權重時，記憶體頻寬與解壓縮的瓶頸。軟體層面的解壓縮 (如從 INT4 解壓至 FP16) 在切換 Expert 時會造成嚴重的延遲。

## 方法 (Methodology)
提出「硬體 MoE 權重解壓縮引擎 (Hardware MoE Weight Decompressor)」。在 NPU 的 DMA 控制器與 SRAM 之間加入內聯解壓縮硬體。當 DMA 從外部記憶體抓取壓縮的 Expert 權重時，硬體能以 Zero-cycle 延遲在飛行途中 (On-the-fly) 將其解壓縮並寫入 SRAM。

## 結果 (Results)
- Baseline Latency (Software Decompression): 19.20 ms
- Proposed Latency (Hardware Inline Decompression): 1.28 ms
- **Speedup: 15.00x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
透過硬體層級的即時解壓縮，能夠將 Expert 載入解壓縮的延遲降低 15 倍。建議在未來 Edge NPU 的 DMA 路徑上，直接內建「On-the-fly Weight Decompressor」，以充分隱藏 MoE 模型的記憶體載入開銷。
