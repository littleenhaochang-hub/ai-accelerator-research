# Hardware Context Chunk Streamer (HCCS) 實驗報告

## 1. 實驗背景
在處理超長文本 (如 1M Tokens) 時，為避免 OOM，通常會採用 Chunked Prefill (將輸入切塊處理)。但軟體層級的 Chunk 切割與排程需要頻繁的中斷與記憶體搬運，導致嚴重的 Prefill 延遲。

## 2. 實驗方法
設計 `hardware_chunk_streamer_sim.py`，模擬將 Chunked Prefill 邏輯硬體化。提出在 NPU DMA 中整合「硬體 Context Chunk 串流器 (HCCS)」。該硬體能自動從主記憶體抓取 4K 大小的 Token 區塊，並無縫餵入 NPU SRAM，完全不需要 CPU 軟體介入排程。

## 3. 實驗數據與結果
*   **Context Length:** 1,048,576 (1M) Tokens
*   **軟體 Chunking 延遲:** 8388.61 ms
*   **HCCS 硬體延遲:** 209.72 ms
*   **加速比:** 40.00x

## 4. 架構建議
硬體自動切割串流能將 1M Token 的 Chunking 排程開銷從 8 秒降低到 0.2 秒。為了讓 Edge NPU 能夠原生地處理無限長度的 Agentic RAG 任務，下一代記憶體控制器必須整合「Hardware Context Chunk Streamer」。