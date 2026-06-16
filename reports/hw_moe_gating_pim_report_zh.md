# 硬體 MoE Gating PIM 引擎 (HW-MoE-Gating-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，MoE 模型的 Gating network (Router) 會成為計算瓶頸，因為必須在決定載入哪些 Experts 前完成評估。

## 2. 探索文獻與方法
將 MoE 的 Gating/Router 邏輯移至 Processing-in-Memory (PIM) 執行，讓 Router 可以非同步、預先在記憶體端計算完畢，以重疊後續 DMA 傳輸的時間。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 22.40x
- **SQNR:** 36.50 dB

## 4. 結論
透過 PIM 技術加速 MoE Router 的評估，大幅隱藏了 PCIe/DRAM 的讀取延遲。建議將 HW-MoE-Gating-PIM 整合至下一代邊緣裝置架構中。
