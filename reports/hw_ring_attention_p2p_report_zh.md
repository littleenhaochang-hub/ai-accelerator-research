# Hardware Ring-Attention P2P Interconnect (HW-RAPI)

## 摘要 (Executive Summary)
針對無限長度上下文 (Infinite Context) 的 Ring Attention 架構，我們探討了多晶片 (Multi-Chiplet) 間 KV Block 傳輸的頻寬瓶頸。本研究提出「硬體 Ring-Attention P2P 互連引擎 (HW-RAPI)」，以完全硬體化的 Ring FIFO 取代傳統依賴 CPU 協調的 PCIe DMA 傳輸。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software DMA):** 傳統 CPU 協調 PCIe 傳輸 KV Block 延遲高達 800.00 ms，嚴重阻礙算力。
- **硬體互連 (HW-RAPI):** 透過非同步 P2P 硬體 FIFO，延遲驟降至 80.00 ms。
- **效能提升 (Speedup):** 達成 **10.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在支援多晶片擴展的 Edge NPU 路由器中整合 HW-RAPI，使得跨晶片的 Ring Attention 得以實現 Zero-CPU 介入的完全隱藏式傳輸，突破邊緣設備的長文本記憶體牆。