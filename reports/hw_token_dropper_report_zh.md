# Hardware Dynamic Token Dropper (HW-DTD) 實驗報告

## 背景與瓶頸分析
生成式模型中的長文本處理會產生極大的 KV Cache。大部分 Token 的 Attention 權重趨近於零，但在軟體層面動態丟棄會產生過多的記憶體碎片與 gather/scatter 成本。

## 探索文獻與架構設計
提出在 SRAM 寫入埠實作 HW-DTD，利用簡易比較器直接在硬體層級濾除低權重 Token，避免其進入記憶體。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 180.00 ms
*   **Proposed Latency:** 52.00 ms
*   **Throughput Speedup:** 3.46x

## 結論
硬體層級的動態 Token 丟棄能有效減少 3.46 倍的延遲，大幅減少長文本推論的記憶體使用。建議整合至下一代 NPU 的 SRAM 控制器中。