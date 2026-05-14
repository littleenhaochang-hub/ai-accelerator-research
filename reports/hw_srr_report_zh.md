# Hardware Semantic RAG Router (HW-SRR)

## 實驗背景 (Background)
在 Agentic AI 工作流中，檢索增強生成 (RAG) 常常需要比對成千上萬個文本區塊 (Chunks)。若交由 CPU 或 NPU MAC 陣列進行軟體層面的餘弦相似度計算與排序，會造成嚴重的延遲與上下文切換瓶頸。

## 實驗設計 (Methodology)
本實驗設計了硬體級別的 RAG 語義路由器 (`hw_srr_sim.py`)。透過在 NPU 記憶體控制器旁整合 Content-Addressable Memory (CAM) 與平行加法樹 (Adder Trees)，能直接在記憶體讀取階段平行計算 Embedding 相似度，並硬體過濾掉無關的 Chunks。

## 實驗結果 (Results)
- Software RAG Filtering (8192 chunks): 0.0234 s
- HW-SRR Latency: 0.0006 s
- **Speedup**: 40.06x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 前端整合「HW-SRR 引擎」，作為 Agentic AI 的專用 Context Filter。這不僅減少了 40 倍的檢索延遲，更節省了將無效 RAG Chunks 搬運至 SRAM 與 Tensor Cores 的龐大能量消耗。