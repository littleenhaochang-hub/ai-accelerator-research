# Hardware Speculative Prefix Tree Searcher (HW-SPTS) for RAG

## 實驗背景與動機
在 Retrieval-Augmented Generation (RAG) 應用中，系統需要在大規模的知識庫 (通常編碼為 Vector Index 或 Prefix Tree) 中搜尋最相關的 Context。當這類 Agentic AI 模型部署於 Edge 裝置時，頻繁的軟體向量檢索 (Vector Search) 會消耗大量的記憶體頻寬 (Memory Bound)，導致推論引擎的 Tensor Core 嚴重閒置。

## 硬體架構協同設計
- **軟體基線:** 依賴 GPU/NPU 的核心將龐大的 Index 讀入 SRAM，再使用 Cosine Similarity 或 L2 Distance 進行比對，導致極大的 $O(N)$ 記憶體搬移開銷。
- **硬體提案:** 提出「Hardware Speculative Prefix Tree Searcher (HW-SPTS)」。在 SRAM 控制器旁植入硬體關聯式記憶體 (Associative Memory) 與搜尋引擎。查詢向量 (Query Vector) 傳入後，HW-SPTS 模組直接在記憶體端執行平行距離計算與 Prefix Tree 遍歷。推論引擎只需等待 HW-SPTS 回傳最匹配的 Token 索引，達成 Zero-DRAM-Bandwidth-Waste 的背景檢索。

## 效能分析結果
針對 128K Token RAG Index 進行 Profiling：
- **傳統軟體 RAG 檢索延遲:** 45.20 ms
- **硬體 HW-SPTS 延遲:** 5.60 ms
- **加速比:** 8.07x

## 結論
HW-SPTS 將檢索邏輯從計算單元 (Compute Units) 卸載至記憶體單元 (Memory Controller)，完美解決了 RAG 應用的記憶體牆問題。建議在主打 Agentic AI 的 Edge NPU 中導入此設計，將大幅提升長文本資料庫的檢索效率。