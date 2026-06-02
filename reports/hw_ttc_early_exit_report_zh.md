# Hardware Test-Time Compute Early Exit Monitor (HW-TTC-EEM)

## 摘要 (Executive Summary)
本研究針對 System 2 推理模型 (Test-Time Compute) 在邊緣設備 (Edge NPU) 上的運算成本進行優化。System 2 模型通常會生成大量的內部思考 Token (Reasoning Tokens)，導致延遲極高。我們評估了在 NPU 輸出端整合一個硬體級的「Early Exit Monitor (HW-TTC-EEM)」，透過即時計算 Token 輸出的熵值 (Entropy) 與信心水準，在確認邏輯已收斂時，自動中斷後續的無效思考過程。

## 實驗結果 (Simulation Results)
- **測試環境:** 最大 1024 Reasoning Steps
- **完整計算延遲 (Baseline):** 5120.00 ms
- **硬體動態早退延遲 (HW-TTC-EEM):** 2323.00 ms (平均於第 460 步退出)
- **延遲加速比 (Latency Speedup):** 2.20x
- **節省運算功耗 (Energy Saved):** 55.1%

## 結論與架構建議
實驗證明，透過硬體層級的信心與熵值監控，能有效避免軟體評估的延遲，讓 System 2 模型在處理相對簡單的問題時提早結束思考，達成 2.20 倍的加速，並節省超過一半的功耗。
**架構提案:** 建議在下一代專門支援 Agentic AI / System 2 推理的 Edge NPU 輸出端，整合「HW-TTC-EEM 監控引擎」。