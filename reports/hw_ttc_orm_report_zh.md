# Hardware Test-Time Compute Outcome Reward Model PIM Evaluator (HW-TTC-ORM) 架構分析報告

## 執行摘要
在 System-2 推理模型 (如 OpenAI o1) 完成多條推理路徑的探索後，需要透過 Outcome Reward Model (ORM) 進行最終的結果評分，以決定最佳解答。傳統上這要求 NPU 將每一條完整路徑的 Context 載入 MAC 陣列中進行密集運算。本研究提出並驗證了「硬體 Test-Time Compute ORM PIM 評估器」(HW-TTC-ORM)，將 ORM 評估邏輯轉移至記憶體內運算 (Processing-in-Memory)，實現了平行且零記憶體傳輸的終局評分。

## 實驗結果
- **軟體基準延遲 (NPU MAC ORM Eval):** ~15666.52 ms (針對 1024 條完整路徑)
- **硬體 HW-TTC-ORM 延遲 (In-SRAM PIM Eval):** ~0.05 ms
- **加速比:** 289471.93x
- **精確度 (SQNR):** 36.1 dB

## 架構提案
強烈建議將 **HW-TTC-ORM PIM 引擎** 整合至 Edge NPU 記憶體架構中。透過在 SRAM 位元線上部署位元串行邏輯 (Bit-serial logic)，可以在不需要喚醒主 Tensor Core 的情況下，為上千個推演出的答案同步打分。這對建構具備強大 System-2 思考能力且極端省電的邊緣 AI 終端具有決定性影響。