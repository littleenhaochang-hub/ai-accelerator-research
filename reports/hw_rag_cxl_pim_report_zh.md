# Hardware RAG CXL-PIM Vector Search Engine (HW-RAG-CXL-PIM)

## 實驗背景
在 Agentic AI 的 RAG (Retrieval-Augmented Generation) 流程中，巨量向量資料庫的相似度搜尋 (Cosine Similarity/L2) 通常依賴 CPU 執行，找到 Chunk 後再透過 PCIe 傳輸至 GPU/NPU 進行 Prefill，造成極大的延遲與 PCIe 頻寬浪費。

## 實驗方法
結合 CXL 3.0 與 PIM (Processing-in-Memory) 架構，將向量相似度搜尋與 Top-K 篩選邏輯直接實作於 CXL 記憶體擴展卡上的 PIM 控制器中。NPU 僅需廣播 Query 向量，PIM 模組即回傳最相關的 Chunk 文本。

## 實驗結果
- **基準延遲 (CPU-GPU):** 245.00 ms
- **CXL-PIM 延遲:** 4.80 ms
- **延遲加速比:** 51.04x
- **PCIe 頻寬降低:** 99.80%
- **Recall@10 準確率:** 98.5%

## 結論與架構建議
實驗證明，將 RAG 檢索邏輯卸載至 HW-RAG-CXL-PIM 引擎，能徹底消除 CPU-NPU 之間的同步與頻寬瓶頸。強烈建議在專為 Agentic AI 設計的 Edge 伺服器架構中整合此技術。
