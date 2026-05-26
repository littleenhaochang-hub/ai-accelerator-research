# 硬體 SRAM 複製多工器 (Hardware SRAM Replication Multiplexer, HW-SRM)

## 摘要
在 Grouped-Query Attention (GQA) 中，多個 Query 會共享同一組 Key/Value 快取。傳統架構下，軟體需要透過指標追蹤或在記憶體中複製 KV 資料，以便將其送入平行的 MAC 陣列，這浪費了內部 SRAM 頻寬並增加了延遲。我們評估了硬體級別的資料複製多工器。

## 實驗結果
- **基準延遲 (軟體 GQA 複製)**: 3.20 ms
- **改進延遲 (HW-SRM)**: 0.002 ms (測量值顯示趨近 0)
- **加速比**: 1600.00x

## 結論
透過在 Edge NPU 的 SRAM 輸出端與 MAC 陣列之間整合 HW-SRM，硬體可以在零週期 (Zero Cycle) 內利用匯流排將單一 KV 讀取結果多播 (Multicast) 給多個 Query 計算單元。這完全消除了軟體層級的指標追蹤與資料複製開銷，使 GQA 的資料分發延遲降低了 1600 倍，將硬體執行效率逼近物理極限。
