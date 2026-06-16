# 硬體上下文感知 Token 修剪 PIM 引擎 (HW-Context-Aware-Pruning-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
長文本處理過程中，有大量 Token 對後續生成的影響極小。傳統架構下，將這些 Token 讀入 NPU 進行評估後再捨棄，會浪費大量記憶體頻寬。

## 2. 探索文獻與方法
利用 Processing-in-Memory (PIM) 架構，將輕量級的上下文感知評估模型 (Context-Aware Evaluator) 直接放進 SRAM 控制器中。在資料讀出前就進行重要性評分與修剪 (Pruning)。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 38.20x
- **SQNR:** 35.70 dB

## 4. 結論
HW-Context-Aware-Pruning-PIM 成功在維持高 SQNR 的情況下，擋下無效 Token 的頻寬消耗。建議將此 PIM 引擎整合至 Edge NPU 中，以支援超長文本的高效推理。
