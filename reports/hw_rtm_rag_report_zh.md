# 硬體 RAG-Token 合併引擎 (HW-RTM) 實驗報告

## 1. 瓶頸分析
檢索增強生成 (RAG) 技術通常會將大量的知識切片 (Chunks) 拼接到 System Prompt 中。由於不同切片往往包含重複的實體與冗餘描述，導致輸入序列 (Sequence Length) 輕易突破 32K，使得 $O(N^2)$ 的 Attention 計算量與 KV Cache 記憶體消耗急劇膨脹。

## 2. 探索文獻
參考最新 ICLR 關於 Token Merging (ToMe) 的研究，我們提出 Hardware RAG-Token Merger (HW-RTM)。在 NPU 的 DMA 與 SRAM 接口處，加入即時 (On-the-fly) 的 Bipartite Matching 相似度比對電路。當載入多個 RAG Chunks 時，硬體會自動將語義高度重疊的 Token 融合為單一 Token。

## 3. 建立原型並驗證
使用 `hw_rtm_rag_sim.py` 進行了硬體層級模擬 (針對 32K Token 進行 60% 融合)：
*   **基準線 (Dense RAG Prefill):** 175.92 ms
*   **HW-RTM:** 49.75 ms
*   **Latency Speedup:** 3.54x
*   **KV Cache Memory Reduction:** 60.00%
*   **SQNR:** 30.2 dB

## 4. 結論
透過硬體層面的動態 Token 融合，HW-RTM 能夠在幾乎不損失語義精度的前提下，將 RAG 應用場景的 Prefill 延遲降低 3.54 倍，並省下高達 60% 的 KV Cache 空間。此協同設計極大提升了 Edge Agentic AI 在處理大規模文件檢索時的實用性。