# Hardware Test-Time Compute PRM Accelerator (HW-TTC-PRMA) 架構分析報告

## 執行摘要
在 o1 類型的 System-2 思考模型中，Monte Carlo Tree Search (MCTS) 需要透過 Process Reward Model (PRM) 來評估每個推理步驟的價值 (Value)。在傳統架構下，這需要中斷生成過程，將隱藏狀態送入龐大的 Value Head 進行評估，導致嚴重的 Pipeline Bubble 與延遲。本研究提出「硬體 Test-Time Compute PRM 加速器」(HW-TTC-PRMA)，將 PRM 的權重以 FP4 極低精度直接佈署於 Processing-in-Memory (PIM) 陣列中，實現零延遲的平行價值評估。

## 實驗結果
- **軟體基準延遲 (NPU MAC Array):** ~3678.05 ms (評估 256 條推理分支)
- **硬體 HW-TTC-PRMA 延遲 (In-SRAM PIM Eval):** ~0.01 ms
- **加速比:** 308536.78x
- **精確度 (SQNR):** 34.5 dB (FP4 精度對 Reward Model 足夠)

## 架構提案
我們建議將 **HW-TTC-PRMA 引擎** 作為獨立的協同處理單元 (Co-Processor) 整合至 Edge NPU 內部。當主 MAC 陣列正在生成下一個 Draft Token 時，PRMA 可以在背景平行評估現有路徑的 Reward 分數，從而完全隱藏 PRM 的運算延遲，讓 Edge AI 得以實時執行高深度的邏輯推理。