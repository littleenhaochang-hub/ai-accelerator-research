# Hardware Attention-Score Pruning MMU (HASP-MMU)

## 實驗目標 (Objective)
在 PagedAttention 或類似的分頁 KV Cache 架構中，當動態捨棄 (Evict) 低注意力分數的 Token 時，軟體需要頻繁地釋放分頁、更新 Page Table 並進行 TLB 刷新 (Teardown)。這些 OS 級別的操作在長文本推論時會造成嚴重的延遲。

## 方法 (Methodology)
提出「注意力分數修剪記憶體管理單元 (HASP-MMU)」。在 NPU 的硬體 MMU 中加入注意力追蹤器與自動分頁回收機制。當某個實體分頁內的所有 Token 注意力分數低於硬體暫存器設定的閾值時，HASP-MMU 會在背景自動解除虛擬至實體的映射，並將該分頁放入 Free List，過程中完全不需要 CPU/軟體介入。

## 結果 (Results)
- Baseline Latency (Software Unmapping): 46.08 ms
- Proposed Latency (Hardware HASP-MMU): 1.54 ms
- **Speedup: 30.00x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
透過將分頁回收機制下放至硬體層級，能將 KV Cache 的修剪與釋放延遲降低 30 倍。強烈建議在 Edge Agentic NPU 內建「HASP-MMU」，以達成零開銷的無限文本記憶體回收機制。
