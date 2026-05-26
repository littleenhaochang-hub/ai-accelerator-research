# Hardware KV Cache Low-Rank Matrix Approximation (HW-LRMA)

## 摘要 (Executive Summary)
本研究針對長文本生成時 KV Cache 的巨大記憶體頻寬瓶頸，提出將 KV Cache 降維矩陣逼近 (Low-Rank Matrix Approximation) 結合至 Edge NPU 硬體的協同設計。

## 實驗動機 (Motivation)
長文本推論 (Long Context Inference) 受到極大的記憶體容量與頻寬限制。單純的量化 (如 INT4) 不足以支撐 128K 以上的上下文。

## 硬體-軟體協同設計 (Hardware-Software Co-Design)
1. **Model Architecture**: 在注意力機制前引入低秩逼近，將龐大的 KV 矩陣拆解。
2. **Hardware Architecture**: 實作 `HW-LRMA Engine`，將低秩矩陣的還原過程直接嵌入至 SRAM 的讀取埠 (Read Port)，以串流方式即時還原特徵，完全避免將還原後的巨大矩陣寫回 SRAM。

## 實驗結果 (Empirical Results)
- **基準延遲 (Baseline Latency)**: 1300.31 ms
- **硬體延遲 (HW-LRMA Latency)**: 311.93 ms
- **加速比 (Speedup)**: 4.17x
- **信噪比 (SQNR)**: 30.5 dB

## 結論與建議 (Conclusion)
透過硬體級別的低秩逼近還原，我們能有效降低記憶體頻寬需求，達到 4.17 倍的延遲改善。建議在 Edge NPU 記憶體控制器中加入 HW-LRMA 模組。

[Code Traceability: ai-accelerator-research/hw_kv_lrma_sim.py]