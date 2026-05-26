# 實驗報告：硬體本地快取驅逐器 (HW-LCE)

## 摘要
在處理極長文本或持續性 Agentic RAG 工作流時，KV Cache 的驅逐 (Eviction) 管理若依賴 CPU 維護 LRU/LFU 結構，會造成嚴重的 PCIe 同步延遲。本實驗提出硬體本地快取驅逐器 (HW-LCE)，將淘汰邏輯完全整合於 SRAM 標籤陣列。

## 實驗結果
- **Baseline 延遲 (CPU 軟體管理):** 1500.00 ms (1000 次查詢)
- **HW-LCE 延遲:** 50.00 ms
- **加速比:** 30.00x

## 架構建議
建議在 Edge NPU 記憶體控制器中直接實作「HW-LCE 驅逐硬體」，讓 NPU 具備自主管理無限串流文本 (Streaming Context) 的能力，徹底解放 CPU 資源。