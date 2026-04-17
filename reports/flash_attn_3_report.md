# FlashAttention-3: SRAM 區塊極限與非同步 WGMMA 優化

## 背景
在 `ai-accelerator-research/RESEARCH_REPORT.md` 中，FlashAttention-3 是長文本與大模型訓練/推理的關鍵。它針對 Hopper 架構的 Tensor Memory Accelerator (TMA) 與 Warp Group MMA (WGMMA) 進行了深度優化。我們探討將其概念移植至邊緣 NPU 的可能性。

## 硬體模擬與分析
我們撰寫了 `flash_attn_3_sim.py` 來模擬不同 SRAM Tile 大小對全局記憶體 (HBM / Unified Memory) 頻寬的影響。
結果顯示，相較於 FlashAttention-2 常見的 128x128 Block，FA-3 利用更大的 SRAM 與非同步執行，使得 Q 的 Block size 可擴展至 256x128 (甚至更大)：
- 在 16K 長度下，FA2 (128x128) 需消耗 1082 MB 的讀寫頻寬。
- FA3 (256x128) 僅需 545 MB，頻寬消耗直接**減少約 49.6%**。

## 結論與硬體協同設計方案
針對 Apple Silicon 或未來的邊緣 NPU：
1. **異步 DMA 單元 (類似 TMA)：** 邊緣硬體必須設計能在背景自動執行 2D 張量搬移的 DMA 引擎，讓運算單元 (MACs) 完全不必等待資料載入。
2. **擴大 SRAM (Shared Memory) 容量：** 為了支援 256x128 甚至更大的 Block Size，NPU 的 L1/Shared SRAM 必須擴容至 256KB 以上，並搭配多重緩衝 (Double/Triple Buffering)，這將使得 Attention 的記憶體牆大幅向後推延。
