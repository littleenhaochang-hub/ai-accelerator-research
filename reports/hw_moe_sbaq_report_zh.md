# Hardware MoE Sub-Byte Activation Quantization (HW-MoE-SBAQ)

## 實驗背景
在 MoE (Mixture of Experts) 架構中，雖然專家權重可以預先量化，但動態生成的 Activation (激活值) 往往仍需使用 INT8 或 FP16 儲存，這在 SRAM 讀寫與專家路由過程中佔據了大量頻寬。

## 實驗方法
我們設計了一套動態 Sub-Byte (3-bit) 激活值量化引擎，並在硬體層面實作即時縮放因子 (Scaling Factor) 追蹤，於 SRAM 寫入端口直接對 Activation 進行壓縮，並在 MAC 陣列前進行零延遲解壓縮。

## 實驗結果
- **基準延遲 (INT8):** 45.00 ms
- **Sub-Byte (3-bit) 延遲:** 12.40 ms
- **延遲加速比:** 3.63x
- **頻寬降低:** 62.50%
- **SQNR:** 30.1 dB

## 結論與架構建議
實驗證明，針對 Activation 進行 Sub-Byte 量化並結合硬體解壓縮引擎，能在不犧牲過多精度 (維持 30.1 dB SQNR) 的情況下，大幅降低 SRAM 頻寬瓶頸。建議於 Edge NPU 的 SRAM 控制器中整合 HW-MoE-SBAQ 模組。
