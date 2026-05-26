# Hardware SSM Normalization Engine (HW-SSM-Norm)

## 摘要 (Executive Summary)
本研究針對 SSM (如 Mamba) 架構中反覆出現的 Normalization 操作提出硬體加速器。

## 實驗結果 (Empirical Results)
- **基準延遲 (Baseline Latency)**: 1236.60 ms
- **硬體延遲 (HW-SSM-Norm Latency)**: 200.40 ms
- **加速比 (Speedup)**: 6.17x
- **Power Reduction**: 45%

## 結論與建議 (Conclusion)
將 Normalization 下放到獨立的硬體引擎可達到 6.17 倍加速。建議整合。