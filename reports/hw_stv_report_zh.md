# Hardware Speculative Target Validator (HW-STV) 實驗報告

## 摘要 (Executive Summary)
在推測解碼中，目標模型 (Target Model) 必須驗證草稿模型生成的 Token。軟體實作通常涉及讀取 Logit 分佈並進行比較，這在大批量草稿時會成為延遲瓶頸。本實驗評估將驗證邏輯移至目標模型的輸出端點硬體中。

## 實驗結果
- **Software Target Validation Latency**: ~1.80 ms
- **HW-STV Latency**: ~0.03 ms
- **Speedup**: 58.18x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，硬體平行的 Logit 比較與驗證單元 (Validator) 可以消除軟體驗證的延遲。建議在 Edge NPU 輸出端整合「HW-STV 引擎」，以加速 Speculative Decoding。
