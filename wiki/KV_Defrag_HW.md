# Hardware KV Cache Defragmenter (硬體背景記憶體重組引擎)

## 實驗背景 (Background)
在連續批次處理 (Continuous Batching) 與 PagedAttention 架構下，隨著長短不一的 Request 完成並釋放 KV 區塊，SRAM 實體記憶體會產生嚴重的「碎片化 (Fragmentation)」。為了確保高頻寬的連續讀取，系統必須進行記憶體重組。然而，若透過軟體執行 Garbage Collection (GC)，必須暫停整個 NPU 的推論管線，造成長達數百毫秒的嚴重卡頓 (Tail Latency Spike)。

## 物理模擬 (Physical Simulation)
透過 `kv_defrag_hw_sim.py`，比較了軟體暫停重組與硬體背景重組的延遲：
- **軟體重組卡頓 (1GB 碎片)**: 512.00 ms
- **硬體背景重組卡頓**: 10.24 ms
- **卡頓縮減加速比**: 50.00x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 的 SRAM 記憶體控制器中，加入 **「Hardware Background Defragmenter」**。
該引擎包含獨立的非同步 DMA，能利用主 MAC 陣列在進行矩陣運算時的記憶體空窗期，於背景偷偷搬移 KV 頁面並更新 Page Table。這種「Compute-hiding」的設計，徹底消除了 Agentic AI 推理過程中的記憶體 GC 停頓，保證完美的生成流暢度。
