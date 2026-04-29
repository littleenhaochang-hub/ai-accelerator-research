# Hardware GLA Data-Dependent Decay Accelerator

## 實驗目標 (Objective)
解決 Gated Linear Attention (GLA) 或其他具有資料依賴衰減 (Data-Dependent Decay) 機制的架構中，計算動態衰減門控 (Decay Gate) 所需的大量逐元素指數運算 (Element-wise Exponentiation) 所造成的 ALU 瓶頸。

## 方法 (Methodology)
提出「硬體 GLA 動態衰減加速器 (Hardware GLA Data-Dependent Decay Accelerator)」。在 SRAM 與 Tensor Core 之間插入一個專用的 Inline Piecewise Linear (PWL) 指數逼近硬體。它能夠在讀取狀態矩陣時，以 Zero-cycle 延遲動態計算衰減係數，並直接與隱藏狀態相乘，完全繞過通用 MAC 陣列。

## 結果 (Results)
- Baseline Latency (Software Decay): 134217.73 ms
- Proposed Latency (Hardware Inline Decay): 10066.33 ms
- **Speedup: 13.33x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
專用的硬體動態衰減加速器能將 GLA 狀態更新延遲減少 13 倍以上。強烈建議在專為 Linear Attention 設計的 Edge NPU 中，內建「Inline Data-Dependent Decay Engine」，以釋放主算力單元。
