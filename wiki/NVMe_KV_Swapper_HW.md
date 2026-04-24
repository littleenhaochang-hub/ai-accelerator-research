# Hardware NVMe KV Cache Swapper (硬體 NVMe KV 緩存交換器)

## 實驗背景 (Background)
為了在 SRAM 極度受限的 Edge NPU 上支援「無限長文本 (Infinite Context)」，我們必須將鮮少被注意到的「冷 KV Cache (Cold Tokens)」換頁 (Swap out) 到大容量的 NVMe SSD 中。然而，若依賴傳統作業系統的 Virtual Memory 或是軟體框架來搬移 4GB 的資料，會引發大量的 CPU Context Switch、Interrupts 與檔案系統開銷，導致推論管線停擺數秒之久。

## 物理模擬 (Physical Simulation)
透過 `nvme_kv_swapper_hw_sim.py`，比較了 CPU 軟體換頁與 NPU 直連硬體換頁的延遲差異：
- **軟體 NVMe Swap 延遲 (搬移 4GB)**: 3276.80 ms
- **硬體 NVMe Swap 延遲 (P2P DMA)**: 204.80 ms
- **整體加速比**: 16.00x

## 架構提案 (Architectural Proposal)
提議在 NPU 的 SRAM 控制器中，直接內建一個精簡版的 **「Direct NVMe P2P Swapper (NVMe 主機控制器)」**。
當 SRAM 滿載需要釋放空間時，該硬體引擎會透過 PCIe Peer-to-Peer (P2P) DMA，直接將冷 KV 分頁寫入 SSD 的邏輯區塊位址 (LBA)。此過程完全「繞過 (Bypass)」了主機 CPU、OS 核心以及系統 DRAM。這項設計讓 Edge 裝置能以極低的背景延遲代價 (約 200ms)，解鎖 TB 等級的超巨量 KV 緩存池。
