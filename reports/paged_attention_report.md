# PagedAttention Hardware MMU Report
## 背景 (Background)
PagedAttention 解決了 LLM 推論中 KV Cache 嚴重的記憶體碎裂 (Memory Fragmentation) 問題。傳統推論框架必須為每個 Request 預先分配最大序列長度的連續記憶體。

## 模擬參數 (Parameters)
- Batch Size: 32
- Max Seq Length: 2048
- Avg Seq Length: 512
- Page Size: 16 tokens

## 模擬結果 (Results)
- 連續記憶體配置 (Contiguous): 1024.00 MB
- 分頁記憶體配置 (Paged): 256.00 MB
- 記憶體使用效率提升: 4.00x

## 架構建議 (Architectural Proposal)
為了讓 Edge NPU 原生支援 PagedAttention，NPU 內部必須實作專屬的 **Hardware MMU (Memory Management Unit) for Tensors**。這允許 NPU 的 DMA 引擎直接使用 Page Table 來讀取分散的 KV Cache Blocks，無需依賴 CPU 介入進行虛擬位址到實體位址的轉換，徹底消除 OS 層級的 Context Switch 延遲。
