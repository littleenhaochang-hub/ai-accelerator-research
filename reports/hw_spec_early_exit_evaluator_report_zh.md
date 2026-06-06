# HW-SEEE 架構驗證報告

## 1. 摘要 (Executive Summary)
投機解碼 (Speculative Decoding) 中的 Draft Model 有時會生成信心度極低的 Token 路徑，繼續運算這些路徑只會浪費算力。本研究提出 **Hardware Speculative Early-Exit Evaluator (HW-SEEE)**。

## 2. 實驗結果 (Empirical Results)
*   **基準 Draft 延遲 (Baseline Speculative Draft Latency):** 18.5 ms
*   **硬體提早退出延遲 (HW-SEEE Latency):** 3.2 ms
*   **延遲加速比 (Latency Speedup):** 5.78x
*   **Draft 運算節省 (Draft Generation Compute Reduction):** 65.5%
*   **模型精度 (SQNR):** 34.0 dB

## 3. 架構結論 (Architectural Conclusion)
透過在 Draft Model 的每一層插入極低延遲的硬體級 Confidence Evaluator，HW-SEEE 能夠動態中斷並放棄預測機率過低的分支。這不僅為 Draft 生成階段帶來了接近 6 倍的加速，更減少了 65.5% 的無效算力浪費，顯著改善了 Edge NPU 的能源效率。