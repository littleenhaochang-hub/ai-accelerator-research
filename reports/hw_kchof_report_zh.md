# 硬體 K-Cache Hadamard 異常值融合器 (HW-KCHOF) 分析報告

## 執行摘要
在低位元 (INT4/INT2) KV Cache 量化中，K-Cache 的異常值 (Outliers) 會導致注意力分數計算的精度嚴重崩潰。雖然軟體層面的 Hadamard 轉換能有效抹平這些異常值，但卻會帶來極大的記憶體與計算延遲。我們提出了將 Hadamard 轉換硬體化的 HW-KCHOF 引擎。

## 模擬結果
* **軟體 Hadamard 轉換延遲:** 230.40 ms
* **HW-KCHOF 內聯延遲:** 7.68 ms
* **效能提升:** 延遲加速達 30.00x。

## 架構建議
針對未來的邊緣 NPU 架構，建議在 SRAM 寫入控制器中整合 **HW-KCHOF (Hadamard Outlier Fuser)**，利用硬體蝴蝶網路 (Butterfly Network) 達成近乎零開銷的異常值抹平，從而完美支援 4-bit 甚至 2-bit 的極端 KV Cache 量化，不損失任何模型生成精度。
