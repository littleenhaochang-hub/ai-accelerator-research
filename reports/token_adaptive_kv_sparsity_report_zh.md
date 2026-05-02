# Token-Adaptive KV Cache Sparsity Hardware 模擬報告

## 摘要 (Executive Summary)
本報告探討了基於 Token 自適應的 KV Cache 稀疏化硬體架構 (Token-Adaptive KV Cache Sparsity Hardware)。在處理超長文本 (128K context) 時，傳統 O(N^2) 的注意力機制會產生巨大的記憶體與運算瓶頸。

## 實驗設計 (Experimental Design)
- **Baseline**: 傳統密集注意力運算，無稀疏化。
- **Hardware-Software Co-design**: 實作動態硬體路由，跳過低重要性的 Token KV 取用，稀疏率設定為 75%。
- **Metric**: 運算加速比 (Speedup) 與訊號量化雜訊比 (SQNR)。

## 實驗結果 (Results)
- **Baseline Latency**: 16.38 s
- **Sparse Latency**: 4.91 s
- **Speedup**: 3.33x
- **SQNR**: 31.25 dB

## 架構建議 (Architectural Proposal)
實驗證明，導入 75% 的稀疏率可以實現 3.33 倍的加速比，且 SQNR 維持在 31.25 dB 的可接受範圍。建議在 Edge NPU 記憶體控制器中整合「Hardware Token-Adaptive Sparsity Router」，以硬體層級直接過濾低權重 Token，避免冗餘的 SRAM 讀取與 MAC 運算。