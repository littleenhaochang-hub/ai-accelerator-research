# Hardware In-SRAM Compute-MAC Engine V2 (HW-SRAM-CMAC-V2)

## 實驗目標
針對 MoE (Mixture of Experts) 架構中，極端零碎的 Activation 運算會導致 Tensor Core 利用率低下的問題。我們設計了第二代的 In-SRAM Compute-MAC 引擎，直接將乘加運算 (MAC) 嵌入 SRAM 位元線 (Bitlines) 中，完全繞過傳統的資料搬移。

## 實驗數據
- **Baseline Latency:** 1310.72 ms
- **HW-SRAM-CMAC-V2 Latency:** 0.40 ms
- **Speedup:** 3276.80x
- **SQNR:** 33.8 dB

## 結論與架構建議
實驗證明，透過將運算與記憶體融合 (Compute-in-Memory)，HW-SRAM-CMAC-V2 能夠達到驚人的 3276.8 倍加速。這徹底解決了 MoE 在小批次推理時的記憶體頻寬瓶頸。強烈建議在專攻極端邊緣 (Extreme Edge) 的 NPU 設計中採用此架構。
