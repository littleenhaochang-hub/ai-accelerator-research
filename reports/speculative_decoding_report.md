# Speculative Decoding Simulation Report
## 背景 (Background)
Speculative Decoding 透過一個輕量級的 Draft 模型預測 tokens，再由大型 Target 模型平行驗證，可突破 Autoregressive Decoding 的 Memory Bandwidth 瓶頸。

## 模擬參數 (Parameters)
- Gamma (Draft Model Lookahead): 4
- Acceptance Rate: 0.7
- Draft Model Token Latency: 2.0 ms
- Target Model Token/Batch Latency: 10.0 ms

## 結果 (Results)
- Baseline 總延遲: 10000.00 ms
- 預測解碼總延遲: 6624.00 ms
- 加速比: 1.51x

## 架構建議 (Architectural Proposal)
為了極大化 Speculative Decoding 的效益，硬體架構應該支援 **Asymmetric Dual-Engine Execution**。Draft Model (小模型) 應完全駐留在高頻 SRAM 或快取中，利用專屬的低精度 (INT4/INT2) Scalar/Vector 單元進行極速自回歸推論；而 Target Model (大模型) 則批次載入權重，利用高頻寬的 Matrix 單元進行平行驗證。這種異質計算架構能最大化 Memory Bandwidth Utilization。
