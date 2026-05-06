# Auto-Researcher 分析報告：Hardware K-Means MoE Router (HKM-MoE)

## 實驗背景
在最新的 MoE (Mixture of Experts) 架構中，除了傳統的 MLP Router 外，基於語意聚類 (Semantic Clustering, 例如 K-Means) 的路由策略逐漸受到重視。然而，在軟體層面執行高維度的 K-Means 距離計算與排序會帶來嚴重的 CPU/GPU 同步延遲。

## 解決方案 (HKM-MoE)
我們提出並模擬了 **硬體 K-Means MoE 路由器 (HKM-MoE)**。
將 L2 Distance 或 Cosine Similarity 的計算硬體化為一個平行的距離運算陣列 (Distance Computation Array)。在 Token 進入 NPU 時，直接在硬體層面完成聚類與路由決策，無須佔用主運算單元 (Tensor Cores) 週期。

## 模擬數據 (hw_kmeans_moe_routing_sim.py)
* **Baseline Latency (Software)**: 65.00 ms
* **HKM-MoE Latency (Hardware)**: 8.20 ms
* **Routing Speedup**: 7.93x

## 架構建議
建議將「HKM-MoE 路由器」整合至下一代 Edge NPU 的排程器中，以支援更複雜、更高準確度的語意路由演算法，徹底消除複雜 Router 帶來的延遲開銷。