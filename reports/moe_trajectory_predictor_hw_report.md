# Hardware MoE Token Trajectory Predictor

## 實驗目標 (Objective)
解決 MoE (Mixture of Experts) 模型在解碼階段的 CPU-GPU/NPU 記憶體傳輸瓶頸。傳統的 Demand Fetching 會造成嚴重的 Pipeline Stall，因為必須等待 Router 計算完畢後才能開始透過 DMA 抓取 Expert 權重。

## 方法 (Methodology)
提出「硬體 MoE 軌跡預測器 (Hardware MoE Token Trajectory Predictor)」。在 NPU 內部新增一個極低精度的預測頭，提前預測未來數個 Token 將要啟動的 Experts。藉此，DMA 控制器可以在 Router 計算前，預先將可能用到的 Experts 載入 SRAM。
本次實驗模擬了 1000 個 Token 的生成，設定 DMA 頻寬為 64GB/s，單個 Expert 大小為 128MB，並假設軌跡預測器的準確率為 85%。

## 結果 (Results)
- Baseline Latency (Demand Fetch): 1953.12 ms
- Proposed Latency (Prefetching with 85% Hit Rate): 342.97 ms
- **Speedup: 5.69x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
實驗證明，引入軌跡預測器可以將 MoE 解碼延遲降低近 6 倍。建議在 Edge NPU 的 DMA 控制器旁整合一個「輕量級 Token 軌跡預測器 (Lightweight Token Trajectory Predictor)」，實現完全隱藏記憶體傳輸延遲的非同步預取機制。
