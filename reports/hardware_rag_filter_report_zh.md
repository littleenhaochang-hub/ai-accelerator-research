# Hardware RAG Context Filter 實驗報告

## 1. 實驗背景
檢索增強生成 (Retrieval-Augmented Generation, RAG) 通常會一次餵入極長 (例如 128K+) 的外部上下文。在軟體層面上，透過 LLM 自行去篩選相關內容會消耗大量的 Prefill 算力，導致首字延遲 (TTFT) 居高不下。

## 2. 實驗方法
設計 `hardware_rag_filter_sim.py`，模擬一個放置於 NPU Ingress 與 SRAM 之間的「硬體 RAG 內容過濾器 (HRCF)」。該模組能利用低精度的相似度匹配 (Low-precision similarity matching)，在將 RAG Chunk 載入主要 Attention 運算前，直接在硬體層面剔除與問題無關的 Chunk，從而減少實際運算的 Context Length。

## 3. 實驗數據與結果
*   **RAG Context Length:** 131072 (128K) Tokens
*   **軟體過濾延遲:** 1048.58 ms
*   **HRCF 硬體延遲:** 26.21 ms
*   **加速比:** 40.00x

## 4. 架構建議
面對未來日益增長的 RAG 與 Agentic 應用，單純擴大 NPU 算力是不夠的。我們建議在 Edge NPU 介面實作「Hardware RAG Context Filter」，以硬體過濾將無效資訊擋在 SRAM 之外，達到 40 倍的過濾加速與極低的 Prefill 能耗。