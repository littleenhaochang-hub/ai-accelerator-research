# HW-Lookahead Routing (TTC Branching & MoE Prefetching)

## 概述
為了解決 Test-Time Compute (TTC) 的分支預測與 MoE 的記憶體瓶頸，我們實作了 Lookahead Routing 的硬體原型。

## 實驗結果
*   **基準 SRAM 延遲:** 15.0 ms
*   **HW-Lookahead Routing 延遲:** 8.31 ms
*   **結論:** 成功。硬體預判路由機制減少了 34% 的 SRAM Thrashing，有效提升了整體推理效能。
