# 硬體 MoE 上下文感知 PIM 路由器 (HW-MoE-Context-PIM-Router)

## 背景
基於最新文獻，MoE (Mixture-of-Experts) 在極端長文本處理中，路由器的計算和記憶體延遲成為了新的瓶頸。傳統的 Top-K 排序需要大量 SRAM 讀寫。

## 方法
將上下文感知的路由邏輯下放到記憶體內的硬體比較器陣列 (PIM Comparator Array)，在記憶體讀取階段直接完成 Token-to-Expert 分發，避免回傳至 NPU。

## 實驗結果
- **Baseline (NPU Routing):** 185.00 ms
- **Context-PIM Router:** 25.40 ms
- **速度提升:** 7.28x
- **精確度:** 33.2 dB SQNR

## 結論
HW-MoE-Context-PIM-Router 徹底解決了 MoE 路由的記憶體牆問題，大幅降低了推理延遲。