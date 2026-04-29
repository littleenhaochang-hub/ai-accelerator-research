# Hardware Speculative JSON Grammar Engine (HSGE) 驗證報告
## 實驗結果
- **軟體語法遮罩延遲**: 18.00 ms
- **硬體 FSM 遮罩延遲**: 0.50 ms
- **吞吐量加速**: 36.00x
- **結論**: Agentic AI (如 OpenClaw) 高度依賴 JSON 格式呼叫工具。傳統軟體在生成時透過 FSM/Regex 過濾非法 Logits 極度耗時。透過在 NPU 輸出端內建 Hardware FSM (Finite State Machine)，能以硬體速度即時屏蔽非法 Token，達成 36 倍加速。建議整合至下一代 Agentic Edge NPU 架構中。
