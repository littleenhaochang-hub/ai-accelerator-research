# Hardware Sparse Token Predictor (HW-STP)

## 實驗背景 (Background)
為了解決 Transformer 模型中 FFN 層的高記憶體頻寬需求與龐大的 MAC 運算量，尤其是 4-bit 權重下的 Outlier 問題，我們需要更有效率的計算方式。

## 實驗設計 (Methodology)
本實驗設計了一個整合超低精度 (INT2) 預測器的硬體架構 (`hw_sparse_token_predictor_sim.py`)。在進入龐大的 FFN MAC 陣列前，預先過濾掉預期輸出接近零的 Token，從而達成動態的稀疏化計算。

## 實驗結果 (Results)
- Dense FFN Latency (32K context): 0.0470 s
- HW-Sparse-Predictor Latency: 0.0071 s
- **Speedup**: 6.65x
- 能量消耗大幅降低，因為避開了 85% 的無效記憶體讀取。

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 的 FFN Block 前端，整合「Hardware Sparse Token Predictor」。利用 INT2 的輕量級神經網路來進行動態 Token 篩選，達成線性級別的加速與功耗優化。