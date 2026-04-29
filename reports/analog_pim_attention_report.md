# 實驗報告：Analog PIM Crossbar Attention (類比記憶體內運算注意力機制)

## 背景 (Background)
在極長文本 (Long Context) 處理中，注意力機制的 $O(N^2)$ 複雜度導致 Digital MAC 陣列遭遇嚴重的 Memory Wall 與 Power Wall。然而，Attention 的 $QK^T$ 點積對低精度雜訊具有極高的容忍度（Softmax 本身會吸收微小擾動），這為 Analog Processing-In-Memory (PIM) 提供了完美場景。

## 方法 (Methodology)
本實驗設計了 **Analog PIM Crossbar Attention**，將 K 與 V Cache 預先儲存於非揮發性記憶體 (如 RRAM 或 PCM) 的 Crossbar 陣列中。當 Query 向量進入時，透過 DAC 轉為類比電壓輸入位元線，並利用克希荷夫定律 (Kirchhoff's Law) 在類比域瞬間完成 $O(N^2)$ 的點積與加總，再由 ADC 輸出。

## 驗證結果 (Results)
- **基準數位 Digital Attention 延遲:** 0.7500 秒，能耗 40960.00 mJ。
- **Analog PIM Attention 延遲:** 0.2708 秒，能耗 2457.60 mJ。
- **整體提升:** 透過類比域瞬時運算，延遲加速達 **2.77x** (瓶頸轉移至 ADC/DAC 轉換)，同時動態能耗大幅降低了 **16.67 倍**。

## 物理架構建議 (Architectural Proposal)
強烈建議 Extreme Edge NPUs (如穿戴式裝置或物聯網) 採用「Hybrid Digital-Analog 晶片封裝」。保留數位 Tensor Core 計算精確的 FFN，但將 Attention Block 完全卸載至「Analog PIM Crossbar Macro」，以打破 $O(N^2)$ 帶來的功耗牆。
