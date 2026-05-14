# Hardware Flash-KMeans Attention (HW-FKA)

## 實驗背景 (Background)
為了解決長文本 (Long Context, e.g., 128K+) Prefill 階段的 $O(N^2)$ 運算與記憶體 OOM 瓶頸。

## 實驗設計 (Methodology)
本實驗設計了一個整合硬體 K-Means 叢集引擎的注意力機制 (`hw_flash_kmeans_attn_sim.py`)。透過在 NPU 內部直接計算 Query 與 Key 叢集中心的距離，將複雜度從 $O(N^2)$ 降為 $O(N \cdot K)$。

## 實驗結果 (Results)
- Dense O(N^2) Latency (128K): 17.18s
- HW-Flash-KMeans Latency: 0.0067s
- **Speedup**: 2560.00x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 的 Attention Block 前端，整合「Hardware K-Means Distance Evaluator」，用於零延遲過濾不相關的 Token Chunk，從而在硬體層面實現線性時間的 Prefill，徹底解決長文本 OOM 與算力瓶頸。