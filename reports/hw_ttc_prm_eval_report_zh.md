# Hardware Test-Time Compute PRM Evaluator (HW-TTC-PRM)

## 摘要 (Executive Summary)
本研究探討在邊緣裝置 (Edge NPU) 執行 System-2 (Test-Time Compute) 推理時，過程獎勵模型 (Process Reward Model, PRM) 評估帶來的瓶頸。傳統上，評估大量平行推理路徑 (Reasoning Paths) 會嚴重佔用 MAC 陣列，導致生成速度大幅下降。我們評估了整合專用的 Inline Value ALUs 來進行硬體級平行 PRM 評估。

## 實驗結果 (Simulation Results)
- **測試環境:** 256 Reasoning Paths
- **軟體 PRM 評估延遲 (Baseline):** 384.00 ms
- **硬體 PRM 評估延遲 (HW-TTC-PRM):** 15.36 ms
- **延遲加速比 (Latency Speedup):** 25.00x
- **獎勵準確度下降 (Reward Accuracy Degradation):** < 0.025%

## 結論與架構建議
實驗證明，透過專用硬體平行評估 PRM，可將 Test-Time Compute 的延遲降低 25 倍，且評估準確率幾乎沒有衰減。
**架構提案:** 建議在專門處理 Agentic AI 邏輯推理的 Edge NPU 排程器中整合「HW-TTC-PRM 引擎」，實現大規模的 System-2 推理加速。