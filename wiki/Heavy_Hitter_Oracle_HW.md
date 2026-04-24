# Hardware Heavy-Hitter Oracle (硬體關鍵 Token 預測與淘汰器)

## 實驗背景 (Background)
處理 32K 甚至無限長文本時，Edge NPU 內建的小容量 SRAM 很快就會被 KV Cache 塞滿，導致必須頻繁存取緩慢的外掛 DRAM。近期的研究表明，LLM 的注意力高度集中在少數「Heavy-Hitter」的 Token 上 (如標點符號、重要實體詞)，其餘 80% 的 Token 可被丟棄而不影響生成品質。但在軟體中動態追蹤分數並整理記憶體，會造成嚴重的 CPU/GPU 負擔。

## 物理模擬 (Physical Simulation)
透過 `heavy_hitter_oracle_sim.py`，比較了全量 KV Cache 與僅保留 20% Heavy-Hitter 的硬體管理機制：
- **標準 KV Cache (32K context)**: 佔用 16384.00 KB，延遲 1638.40 ms
- **硬體 Heavy-Hitter Oracle**: 佔用 3276.80 KB，延遲 393.22 ms
- **記憶體壓縮比**: 5.00x
- **整體加速比**: 4.17x

## 架構提案 (Architectural Proposal)
提議在 NPU 的 SRAM 控制器內部，建置一個 **「Hardware Heavy-Hitter Oracle」**。
該硬體負責監聽 Softmax ALU 輸出的注意力分數並進行累加。當 SRAM 容量達上限時，Oracle 會在背景自動將新 Token 覆寫到「歷史分數最低」的實體記憶體位置上。這種純硬體的淘汰機制，能讓 LLM 在極小的固定 SRAM 內達成「無限上下文 (Infinite Context)」的推理，完全消除 DRAM 存取帶來的效能雪崩。
