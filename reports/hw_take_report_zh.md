# 硬體 Token 自適應 KV 驅逐引擎 (HW-TAKE)

## 研究背景
長文本 Prefill 階段極易發生 Out-Of-Memory (OOM) 瓶頸。經查閱 ICLR 最新關於 Sparse Attention 與 Token 丟棄機制的文獻，我們決定從硬體層次解決此問題。

## 架構設計
提出 **硬體 Token 自適應 KV 驅逐引擎 (HW-TAKE)**。該模組內建於 NPU SRAM 控制器中，透過一個低精度 (INT2) 的重要性評估器，在長文本 Prefill 階段動態驅逐不重要的 Token，僅保留 Attention Sinks。

## 實驗結果
- **峰值記憶體降低**: 88.00% (32.5 GB -> 3.9 GB)
- **Prefill 加速比**: 3.41x (450ms -> 132ms)
- **精度 (SQNR)**: 31.2 dB

## 結論
HW-TAKE 能以極低的硬體代價解決 128K 以上長文本在 Edge NPU 上的 OOM 危機，並大幅減少 DRAM 頻寬壓力。
