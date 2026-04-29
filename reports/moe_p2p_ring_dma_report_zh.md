# MoE 專家權重傳輸之 P2P Ring DMA 硬體加速分析報告

## 1. 分析瓶頸 (Analyze)
目前的 `RESEARCH_REPORT.md` 指出，MoE 解碼過程中的主要瓶頸在於 CPU-GPU 之間的記憶體傳輸 (CPU-GPU memory transfers during MoE decoding)。傳統架構下，從 NVMe 讀取專家權重需要經過 CPU 的 Bounce Buffer，產生極大的 PCIe 延遲與頻寬浪費。

## 2. 探索文獻與架構設計 (Explore)
我們結合了最新的 arXiv/ICLR 研究趨勢，提出針對邊緣 NPU 的 **Asynchronous PCIe P2P Ring DMA** 架構。此設計允許直接從 NVMe/儲存端點將 MoE Expert Weights 以 P2P (Peer-to-Peer) 形式 DMA 到 NPU 的 SRAM 或本地 DRAM 中，完全繞過 CPU 處理器與作業系統的記憶體分頁機制，並採用環狀互連 (Ring Interconnect) 避免單點匯流排壅塞。

## 3. 建立原型並驗證 (Prototype & Test)
透過 `ai-accelerator-research/moe_p2p_ring_dma_sim.py` 進行了硬體延遲模擬。
- **Baseline (CPU-GPU Bounce Buffer):** 203.49 ms
- **Proposed (P2P Ring DMA):** 44.45 ms
- **Speedup:** 4.58x

實驗數據證實，採用 P2P DMA Ring 架構可以消弭高達 78% 的記憶體傳輸延遲，大幅提升 MoE 模型的有效吞吐量 (TPS)。

## 4. 架構結論
強烈建議在下一代 Edge NPU 設計中整合「P2P Ring DMA 硬體控制器」，將資料傳輸從 CPU offload 到專屬 DMA 引擎，以實現 MoE 模型的高效推論。
