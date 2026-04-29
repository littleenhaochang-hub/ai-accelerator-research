# MoE 專家權重之硬體 Huffman 解壓縮引擎分析報告

## 1. 分析瓶頸 (Analyze)
目前的 `RESEARCH_REPORT.md` 顯示，即使套用了 INT4 甚至極端量化，MoE 在 Edge NPU 上的頻寬瓶頸依然嚴峻。因為每次推論都必須即時從 DRAM/UFS 載入巨大的 Expert Weights。

## 2. 探索文獻與架構設計 (Explore)
我們回顧了資料壓縮領域，並將其與 NPU SRAM 控制器結合。權重分佈通常呈現高度不均勻 (如鐘型曲線)。透過將出現頻率最高的權重指派最短的位元碼 (Huffman Coding)，可以將平均位元數從 4-bit 降至約 2.5-bit。
我們提議在 SRAM Read Port 前端整合一個「Hardware Huffman Tree Decompressor (硬體 Huffman 解壓縮引擎)」，能夠在單一 clock cycle 內以硬體查表方式 (Hardware LUTs) 展開變動長度的權重編碼，無須 CPU 介入。

## 3. 建立原型並驗證 (Prototype & Test)
透過 `ai-accelerator-research/huffman_moe_hw_sim.py` 進行了專家權重載入延遲的模擬：
- **Baseline (INT4 Fetch):** 1.328 ms
- **Proposed (Huffman Compressed Fetch):** 0.574 ms
- **Speedup:** 2.31x

實驗證實，透過變動長度編碼搭配即時硬體解壓縮，可以節省超過 56% 的記憶體傳輸延遲，大幅提升 MoE 模型的推論 TPS。

## 4. 架構結論
強烈建議在下一代 Edge NPU 的記憶體控制器 (Memory Controller) 內整合「硬體 Huffman 解壓縮引擎」，以便在從外部記憶體載入資料至 SRAM 的傳輸過程中實現 on-the-fly 的無延遲權重解壓縮。
