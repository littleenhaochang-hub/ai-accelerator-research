# 針對 MoE CPU-GPU 記憶體傳輸瓶頸的 Processing-in-Memory (PIM) 架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
根據基礎測試，在大型 Mixture-of-Experts (MoE) 模型推論時，頻繁的 expert fetch 會受到 PCIe Gen4 x16 等匯流排頻寬限制。載入單個 128MB 的 Expert 到 GPU SRAM 會造成顯著的延遲（約 1.95ms 傳輸 + 2.5ms 計算），成為解碼階段的最大瓶頸。

## 2. 解決方案：MoE PIM 架構 (Processing-in-Memory)
我們模擬了將簡單的 MAC (Multiply-Accumulate) 單元直接實作於 DRAM 內部（即 Processing-in-Memory, PIM 架構）。這樣一來，我們不需要將 128MB 的 expert 權重搬移到 NPU/GPU 中，而是將只有幾 KB 的 activation (例如 4096 維度，約 0.015MB) 傳送到記憶體端進行計算，再把結果傳回。

## 3. 原型驗證結果 (Prototype Results)
執行腳本：`pim_moe_sim.py`
- **Baseline (PCIe Demand Fetch)**: 每專家耗時約 4.4531 ms
- **PIM 架構**: 每專家耗時約 3.5002 ms
- **資料移動減少 (Data Movement Reduction)**: 8,192 倍
- **整體速度提升 (Speedup)**: 1.27x

雖然 PIM 單元的運算時脈較低導致純計算時間微幅增加 (2.5ms -> 3.5ms)，但徹底消除了權重的傳輸延遲，大幅減少了系統整體的能耗與 PCIe 匯流排佔用。

## 4. 硬體架構建議
對於 Edge NPU，我們建議與記憶體廠商合作，將 "MoE PIM Controller" 整合至系統架構中。對於頻繁觸發的長尾專家群 (Long-tail experts)，直接利用 PIM 計算，而常用的 Shared Experts 則保留在 NPU SRAM 內。
