# Hardware Test-Time Compute Early-Exit Monitor (HW-TTC-EE)
## 針對 System 2 推理過度運算的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
Test-Time Compute (System 2 推理) 模型被賦予預先定義的「思考預算」(Reasoning Budget，如 2048 步)。然而，並非所有查詢都同樣複雜，許多簡單的問題在前期就已得出高信心答案。強迫模型跑滿預算是對 Edge 裝置電量與延遲的極大浪費。

### 2. 探索文獻 (Explore)
我們提出 Hardware Test-Time Compute Early-Exit Monitor (HW-TTC-EE)。透過在 NPU 輸出端整合一個低功耗的「信心熵監控器」(Confidence Entropy Monitor)，硬體會即時評估內部推理狀態的收斂程度。當答案的信心分佈達到預設閾值時，硬體排程器會瞬間觸發 Early Exit，提早結束思考迴圈。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_ttc_ee_sim.py` 進行最大 2048 步的模擬驗證：
- **Baseline TTC Latency:** 30720.00 ms
- **HW-TTC-EE Latency:** 4610.00 ms
- **Speedup (加速比):** 6.66x
- **總耗能縮減:** 85.0%

### 4. 結論
實作 HW-TTC-EE 能夠帶來 6.66x 的加速比，並節省 85% 的推理功耗。建議將此「動態提早退出監控器」作為標準配備，整合入下一代 Edge NPU 中，以最大化行動裝置上的 Agentic AI 續航力。
