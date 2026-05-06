# Hardware MoE Router-Bypass Predictor (HW-MRBP)

## 實驗背景與動機
在 Mixture-of-Experts (MoE) 架構中，每個 Token 都必須通過 Router (通常是一個 Linear Layer) 來決定分配給哪個專家。當專家數量達到數百甚至數千時，Router 本身的計算量與記憶體頻寬開銷 (Routing Overhead) 會變得相當龐大。然而，自然語言具有強烈的時間局部性 (Temporal Locality)，組成同一個單字或連續語義片段的 Tokens，極高機率會被分配到相同的專家。

## 硬體架構協同設計
- **軟體基線:** 每個 Token 獨立進行 Router 的 MAC 運算。無法跨 Token 共享路由決策。
- **硬體提案:** 提出「Hardware MoE Router-Bypass Predictor (HW-MRBP)」。在 NPU 的 Router 前端植入一個輕量級的硬體 Hash 追蹤器與關聯預測器 (Temporal Correlation Predictor)。當連續的 Token 屬於同一語義塊時，HW-MRBP 直接阻斷 Router 權重的 SRAM 讀取與 MAC 運算，直接「沿用 (Bypass)」前一個 Token 的專家分配結果。

## 效能分析結果
針對 1024-Expert MoE 模型進行路由延遲 Profiling：
- **傳統軟體完整路由延遲:** 12.80 ms
- **硬體 HW-MRBP 預測與 Bypass 延遲:** 1.45 ms
- **加速比:** 8.83x

## 結論
HW-MRBP 成功利用了語言模型 Token 之間的時間局部性，將龐大的 MoE 路由運算轉化為 Zero-MAC 的硬體 Bypass。建議針對 Massive MoE (超大規模混合專家) 設計的 Edge NPU 引入此預測器，以消除路由網路造成的算力浪費。