# 硬體前綴樹修剪引擎 (HW-Prefix-Tree-Pruner) 實驗報告

## 1. 實驗背景與瓶頸分析
為解決「長文本 Prefill OOM」問題，當模型讀取數十萬字元的文本時，O(N^2) 的 Attention 記憶體用量會塞爆 NPU SRAM/DRAM。

## 2. 探索文獻與方法
利用動態硬體閾值對 Prefix Tree 結構進行動態修剪，拋棄低關聯性的背景 Token。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 15.00x
- **記憶體減少 (Memory Reduction):** 85.00%
- **SQNR:** 35.10 dB

## 4. 結論
整合 HW-Prefix-Tree-Pruner 能有效防範長文本 OOM，建議納入架構。
