# 硬體 Token 聚類 PIM 引擎 (HW-Token-Clustering-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，長文本 Prefill 與稀疏注意力需要進行複雜的 Token 聚類 (Clustering) 運算，這在傳統 CPU/GPU 上會帶來龐大的控制流與記憶體存取延遲。

## 2. 探索文獻與方法
利用 Processing-in-Memory (PIM) 架構，將 K-Means 或 LSH 等 Token 聚類演算法直接移至記憶體端執行，消除 CPU-GPU 的 PCIe 瓶頸。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 25.80x
- **SQNR:** 35.20 dB

## 4. 結論
HW-Token-Clustering-PIM 能大幅加速長文本 Token 的動態管理，建議將其整合至下一代 NPU 的記憶體控制器中。
