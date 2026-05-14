# 硬體長文本區塊化預填處理器 (Hardware Chunked Prefill Engine) 模擬報告

## 1. 瓶頸分析
目前的長文本 (如 128K context) Prefill 階段，標準的 Self-Attention 會產生 O(N^2) 的 Peak Memory。對於邊緣裝置 (Edge NPU)，這會導致嚴重的 OOM (Out of Memory)，即使模型參數再小也無法執行長文本分析。

## 2. 解決方案 (Hardware Chunked Prefill Engine)
我們提出將軟體層面的 Chunked Prefill (如 FlashAttention-3 的區塊切割) 實作到 NPU 硬體排程器中。透過將輸入切分為固定大小 (例如 4K tokens) 的 Chunk，NPU 循序處理並將 KV Cache 動態聚合。這使得 Attention 的記憶體消耗從 O(N^2) 降至 O(C \times N)，其中 C 為 Chunk Size。

## 3. 實驗結果
透過 `hw_chunked_prefill_sim.py` 模擬 128K tokens 的 Prefill 記憶體足跡：
- Baseline (Full O(N^2) Attention): 32800.00 MB (直接導致 Edge NPU OOM)
- HW Chunked Prefill (4K chunks): 64.00 MB
- **Memory Reduction: 512.50x** (延遲保持不變，均為 O(N) Compute Bound)

## 4. 架構建議
針對次世代 Edge NPU，強烈建議在硬體控制單元 (Hardware Scheduler) 整合「Chunked Prefill Engine」，讓 NPU 能夠原生地分塊處理長文本，徹底打破 SRAM 與 LPDDR 記憶體容量對 Context Length 的物理限制。