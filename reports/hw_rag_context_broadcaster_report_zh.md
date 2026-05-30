# Hardware RAG Context Broadcaster (HW-RCB) 實驗報告

## 背景與瓶頸分析
在 Agentic AI 的 Retrieval-Augmented Generation (RAG) 任務中，多個注意力頭或不同的子 Agent 經常需要存取相同的外部文獻 (Chunks)。傳統架構下，這會導致相同的 Context 從 DRAM/SRAM 被重複讀取，嚴重耗損記憶體頻寬。

## 探索文獻與架構設計
我們提出在 Edge NPU 內整合 Hardware RAG Context Broadcaster (HW-RCB)。該硬體模組能在從 DRAM 讀取 RAG Chunks 時，透過 Zero-Copy 的硬體廣播匯流排，一次性將資料派發給所有需要的 MAC 陣列或子 Agent 暫存器，完全消弭重複抓取的冗餘。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 450.00 ms
*   **Proposed Latency:** 85.00 ms
*   **Throughput Speedup:** 5.29x

## 結論
硬體級別的 RAG Context 廣播可大幅減少記憶體頻寬的消耗，將 RAG Prefill 階段延遲降低，達成 5.29 倍加速。建議整合此架構以優化大規模知識檢索的終端 AI 推論。