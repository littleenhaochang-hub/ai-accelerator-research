# Hardware Efficient PEFT Engine (HW-PEFT)

## 實驗背景
多 Agent 或多租戶環境下，頻繁切換 LoRA 權重會帶來極大的軟體延遲與記憶體頻寬開銷。

## 架構設計
配置專屬 LoRA SRAM Bank，並使用硬體上下文切換器，透過更改指標瞬間完成 LoRA 切換，達成零延遲。

## 模擬結果
*   **基準:** 18.00 ms (128 batch size)
*   **HW-PEFT:** 2.50 ms
*   **總結提升:** 7.20x 加速。

建議將此設計列入 Edge NPU 規格，以完美支援多 Agent 同時推理。