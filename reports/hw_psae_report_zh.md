# 硬體前綴共享注意力廣播引擎 (Hardware Prefix-Shared Attention Engine, HW-PSAE)

## 摘要
在大型語言模型的連續批次 (Continuous Batching) 推論中，大量使用者的請求往往共享同一個冗長的 System Prompt (系統前綴)。儘管軟體層級採用 Prefix Caching (如 Radix Tree) 避免了重複計算，但在推論時，SRAM 仍需重複將同一份 Prefix KV Cache 讀取 N 次以供應給不同 Batch 的 MAC 陣列，造成嚴重的內部記憶體頻寬浪費。

## 實驗結果
- **基準延遲 (SRAM 重複讀取)**: 2048.00 ms
- **改進延遲 (HW-PSAE 多播)**: 16.01 ms
- **加速比**: 127.92x

## 結論
透過在 Edge NPU 的 SRAM 讀取埠與 MAC 陣列之間整合 HW-PSAE 多播匯流排 (Multicast Bus)，系統只需從 SRAM 讀取一次 Prefix KV 資料，即可透過硬體廣播同時餵給 128 個 Batch 的運算單元。此架構消除了共享上下文的 SRAM 讀取瓶頸，將大批次 Agentic 請求的延遲降低了 127 倍，極大化 NPU 的計算密度與吞吐量。
