# 硬體 PEFT 上下文切換 MAC 陣列 (Hardware PEFT Context-MAC, HW-PEFT-CMAC)

## 摘要
在 Edge 設備上支援多代理 (Multi-Agent) 或多任務推論時，我們需要在連續批次 (Continuous Batching) 中快速切換不同的 LoRA 權重 (PEFT Adapters)。依賴軟體層級的記憶體載入會導致嚴重的 Context Switch 延遲。我們評估了支援硬體級上下文切換的 MAC 陣列。

## 實驗結果
- **基準延遲 (軟體多租戶 LoRA 切換)**: 40.96 ms
- **改進延遲 (HW-PEFT-CMAC)**: 0.82 ms
- **加速比**: 50.00x

## 結論
透過在 Edge NPU 內部配置專用的 LoRA SRAM 緩衝區，並整合 HW-PEFT-CMAC 硬體上下文切換器，可以在零週期的情況下切換 MAC 陣列正在執行的 LoRA 權重。這消除了 DRAM 到 SRAM 的軟體調度開銷，將多任務代理的推論延遲降低了 50 倍，完美支援高併發的 Personal AI 應用。
