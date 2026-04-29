# CXL MoE 預先抓取 (Prefetching) 記憶體傳輸優化分析報告

## 1. 實驗背景
目前 Auto-Researcher 報告指出，MoE 模型的推論瓶頸在於 CPU-GPU 之間的記憶體傳輸 (PCIe/CXL)。由於硬體計算時間極短，但 Expert 權重由 Host DRAM 載入至 NPU SRAM 的延遲極高，這造成了嚴重的 I/O-compute 不匹配。我們針對 CXL 頻寬與預測性抓取 (Predictive Prefetching) 的硬體架構進行了模擬。

## 2. 實驗設定
- 實驗腳本：`cxl_moe_prefetch_sim.py`
- 架構參數：PCIe Bandwidth 64GB/s, CXL Bandwidth 128GB/s
- 專家模型大小：100 MB per expert
- 模擬機制：Demand Loading (傳統 PCIe) vs CXL Predictive Prefetching (90% 預測準確率)

## 3. 實驗結果
- **Demand Loading Latency**: 3525.88 ms
- **CXL Prefetching Latency**: 2072.48 ms
- **Speedup**: 1.70x

## 4. 結論與硬體建議
模擬證實，結合 CXL 記憶體擴展與 90% 準確度的硬體預測抓取器，可將延遲降低，達成 1.70 倍的速度提升。
**硬體設計建議：**
建議於 Edge NPU 的 DMA Controller 內整合一組「MoE Lookahead Prefetcher」，利用 Token 軌跡進行提早的 CXL 非同步載入，將 I/O 隱藏於計算背景中。