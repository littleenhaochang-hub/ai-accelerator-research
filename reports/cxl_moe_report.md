# MoE 專家權重的 CXL 3.0 記憶體池架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
繼先前的 PIM 研究後，我們進一步分析了無法置入 PIM 的超大型 MoE 模型 (例如 100B+ 參數，需要 TB 級儲存)。傳統上將這些專家儲存在 NVMe SSD 並透過 PCIe Gen4 DMA 搬移至 GPU SRAM 會面臨巨大的作業系統 (OS) 與 DMA setup 延遲 (約 1.5ms)，這對於需要極低延遲 Token 生成的互動式 AI 來說是致命的。

## 2. 探索與文獻 (Exploration)
我們引入了 **CXL 3.0 (Compute Express Link)** 記憶體語意協定。CXL 允許 NPU 直接使用一般的 Load/Store 指令來存取擴充記憶體池，將設備記憶體與主機記憶體在硬體層級統一，繞過了傳統的 block-based DMA 傳輸與 OS 驅動層。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`cxl_moe_sim.py`
- **PCIe Gen4 (含 DMA 延遲)**: 每專家 fetch 約 3.5015 ms
- **CXL 3.0 (Memory-semantic)**: 每專家 fetch 約 2.0502 ms
- **速度提升 (Speedup)**: **1.71x**

數據證實，雖然兩者實體層頻寬相似 (64GB/s)，但 CXL 3.0 將協議延遲從 1500ns 降至 200ns，並將 OS 負載從 1.5ms 壓縮至 0.05ms，實現了真正的 Byte-addressable expert 存取。

## 4. 系統建議
對於未來的伺服器機櫃與高階 Edge 工作站，強烈建議捨棄 PCIe DMA，全面導入 CXL 3.0 記憶體擴充卡來儲存 MoE 專家矩陣，達成 O(1) 的超低延遲權重交換。
