# Hardware Zero-Copy RLHF Engine (HW-ZC-RLHF)

## 摘要 (Executive Summary)
本研究探討在邊緣裝置 (Edge NPU) 執行 On-device RLHF (Reinforcement Learning from Human Feedback) 時的模型切換瓶頸。RLHF 需要頻繁在 Policy, Reference, Reward, 與 Value 模型間切換，導致嚴重的 SRAM-DRAM 記憶體置換開銷。我們評估了「硬體零拷貝 (Zero-Copy) RLHF 引擎」，透過 3D Stacked SRAM 與暫存器指標切換來達成無縫的 Multi-Model 執行。

## 實驗結果 (Simulation Results)
- **測試環境:** 64 Batch Size
- **軟體模型置換延遲 (Baseline):** 288.00 ms
- **硬體零拷貝延遲 (HW-ZC-RLHF):** 51.20 ms
- **延遲加速比 (Latency Speedup):** 5.62x
- **訊噪比 (SQNR):** 33.8 dB

## 結論與架構建議
實驗證明，透過硬體層級的 Zero-Copy 指標切換，可以將 Edge RLHF 的多模型調度開銷降低，並達成 5.62 倍的加速。
**架構提案:** 建議在下一代 Edge NPU 中整合「HW-ZC-RLHF 引擎」，以原生支援設備端的持續學習與人類反饋對齊。