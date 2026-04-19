# 長文本 Prefill OOM：Chunked Prefill 硬體加速報告

## 瓶頸分析
根據 `RESEARCH_REPORT.md`，處理極長文本 (如 128K tokens) 時，Prefill 階段的 Attention 矩陣大小呈 O(N^2) 成長，導致嚴重的 Out-Of-Memory (OOM) 甚至高達 30GB 記憶體消耗，Edge NPU 無法承受。

## 解決方案：硬體 Chunked Prefill 引擎
我們參考最新的長文本優化論文，提出 Chunked Prefill 硬體化方案。將 128K 的輸入切割為 4K 的 Chunks，並在硬體中加入「狀態保留暫存器 (State Retention Registers)」，讓跨 Chunk 的 Attention 可以透過狀態傳遞完成，而非一次性展開整個 NxN 矩陣。

## 實驗結果
透過 Python 模擬 `chunked_prefill_sim.py`：
- **傳統 Prefill 記憶體消耗 (128K Context):** 30.52 GB
- **Chunked Prefill 記憶體消耗 (Chunk = 4K):** 0.98 GB
- **記憶體縮減倍率:** 31.25x

## 結論
硬體層級的 Chunked Prefill 能將 128K 文本的 OOM 危機完全解除，將記憶體消耗控制在 1GB 以內。建議在未來的 NPU 設計中加入「硬體分塊排程器 (Hardware Chunk Scheduler)」。
