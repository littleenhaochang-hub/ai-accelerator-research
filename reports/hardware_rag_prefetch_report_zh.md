# Hardware RAG Chunk Pre-Fetcher (HRCP) 實驗報告

## 1. 實驗背景
在 Agentic AI 的檢索增強生成 (RAG) 流程中，大量的外部知識片段 (Chunks) 需要被拉入 NPU SRAM。傳統上這需要 CPU 多次觸發中斷並設定 PCIe DMA，當 Chunk 數量增加時，會產生嚴重的 I/O 阻塞延遲。

## 2. 實驗方法
設計 `hardware_rag_prefetch_sim.py`，模擬將 RAG 的多區塊抓取邏輯交由 NPU 內建的「硬體 RAG 區塊預取器 (HRCP)」負責。CPU 只需要下達一次 Scatter-Gather 清單，HRCP 會非同步地將所有 RAG Chunks 以 Pipeline 方式拉入 SRAM，完全不需要 CPU 中斷。

## 3. 實驗數據與結果
*   **RAG Chunks 數量:** 256
*   **軟體中斷預取延遲:** 384.00 ms
*   **HRCP 硬體非同步延遲:** 12.80 ms
*   **加速比:** 30.00x

## 4. 架構建議
針對 Agentic RAG 場景的 Edge NPU，強烈建議在 DMA 控制器中整合「Hardware RAG Chunk Pre-Fetcher (HRCP)」，利用非同步 Scatter-Gather 消除 30 倍的 I/O 設定延遲，進一步降低 RAG 的 TTFT (首字延遲)。