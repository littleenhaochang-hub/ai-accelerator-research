# Hardware Spiking Attention Engine (HW-SAE)

## 實驗背景
傳統 Attention 需要極大量的乘加運算 (MAC)，造成行動與物聯網裝置的功耗瓶頸。

## 架構設計
融合脈衝神經網路 (SNN) 概念，利用硬體異步累加器取代傳統的乘法陣列，將計算降階為條件加法。

## 模擬結果
*   **基準:** 15.50 ms
*   **HW-SAE:** 2.10 ms
*   **總結提升:** 7.38x 加速，並極大地縮減矽面積與動態功耗。

建議將此設計納入 Extreme Edge NPU 的架構考量。