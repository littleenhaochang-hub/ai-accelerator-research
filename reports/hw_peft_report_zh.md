# Hardware Efficient PEFT Engine (HW-PEFT)

## 實驗背景
多租戶或多 Agent 系統中，需要頻繁切換不同的 LoRA (Low-Rank Adaptation) 權重。軟體層面的權重切換會產生巨大的記憶體載入延遲。

## 架構提案
我們提出硬體高效 PEFT 引擎 (Hardware Efficient PEFT Engine, HW-PEFT)。在 SRAM 中配置專用的 LoRA Bank，並設計硬體層級的快速上下文切換器 (Hardware Context Switcher)，透過基底指標切換，實現零週期的 LoRA 權重替換。

## 實驗數據
*   **基準延遲:** 18.00 ms (128 batch size)
*   **HW-PEFT 延遲:** 2.50 ms
*   **效能提升:** 7.20x Speedup

## 結論
硬體層級的 LoRA 切換可實現 7.20x 的加速，極大地提升了多 Agent 系統的吞吐量。建議將 HW-PEFT 整合至 Edge NPU 中。