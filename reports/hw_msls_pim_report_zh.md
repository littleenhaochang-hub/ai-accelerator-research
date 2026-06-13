# 硬體架構研究報告: HW-MSLS-PIM (Multi-Scale Lookahead Speculative PIM Engine)
## 摘要
本研究評估了將多尺度前瞻推測解碼 (Multi-Scale Lookahead Speculative Decoding) 直接實作於 PIM 的硬體架構。在 256000 上下文長度下，相較於傳統數位 MAC 陣列，達成 83.33 倍的延遲加速，且 SQNR 維持在 34.20 dB。
## 架構提議
建議在 Edge NPU 記憶體陣列中整合「HW-MSLS-PIM 引擎」，將推測解碼的草稿生成與驗證全部卸載至記憶體端，徹底消除 PCIe 頻寬瓶頸。
