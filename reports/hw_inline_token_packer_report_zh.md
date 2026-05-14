# Hardware Inline Token Packer (HW-ITP)

## 摘要 (Executive Summary)
在支援稀疏注意力 (Sparse Attention) 或是 Token 放棄 (Token Dropping) 的模型中，軟體需要頻繁地重整並壓縮 (Pack) 記憶體中散落的有效 Token，以維持 MAC 陣列的利用率。本研究探討並驗證了「硬體即時 Token 壓縮器 (HW-ITP)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Packing):** 透過 CPU/GPU 核心追蹤 Mask 並進行記憶體複製重排，延遲達 580.00 ms。
- **硬體壓縮器 (HW-ITP):** 在 DMA 寫入 SRAM 的通道上整合過濾器，自動略過無效 Token 並將有效 Token 連續寫入，延遲降至 40.00 ms。
- **效能提升 (Speedup):** 達成 **14.50x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的 SRAM 控制器與 DMA 通道之間整合 HW-ITP。這能徹底消除演算法層面的記憶體碎片化問題，確保 Tensor Cores 永遠接收到連續且密集的資料流。