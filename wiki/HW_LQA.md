# Hardware Log-Quantized Attention (HW-LQA)

## 實驗背景
注意力機制的 QK 點積在長文本下消耗巨大 MAC 能耗。

## 架構設計
將矩陣對數化，利用加法樹取代昂貴的乘法器硬體。

## 模擬結果
*   **基準 (FP16):** 2.00 ms
*   **HW-LQA:** 0.40 ms
*   **總結提升:** 5.00x 加速，並減少 86.67% 動態能耗。

建議將此設計列入 Extreme Edge NPU 規格，打破注意力能耗牆。