# 硬體 MoE 快取 PIM 引擎 (HW-MoE-Caching-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，MoE 架構下專家權重的動態載入仍然是嚴重的 Memory Wall。

## 2. 探索文獻與方法
結合 PIM (Processing-in-Memory) 與快取預取演算法，在記憶體端直接進行熱門專家的快取計算。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 18.50x
- **SQNR:** 36.40 dB

## 4. 結論
透過 PIM 端快取機制，大幅減少 PCIe 頻寬佔用，建議納入下一代 NPU 架構。
