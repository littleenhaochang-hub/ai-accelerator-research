# Hardware Log-Quantized Attention (HW-LQA)

## 實驗背景
注意力機制的 QK 點積需要消耗大量乘加運算 (MAC)，造成嚴重的能耗。我們評估使用對數對齊量化 (Log-Quantization) 將乘法轉換為移位與加法。

## 實驗結果
*   **基準 (FP16):** 2.00 ms, 1.5 pJ/MAC
*   **HW-LQA:** 0.40 ms, 0.2 pJ/Addition
*   **效能提升:** 5.00x 加速，並減少 86.67% 動態能耗。

## 結論
在 Edge NPU 內建對數加法樹 (Log-Adder Trees) 可以有效消除注意力機制的硬體乘法器需求，極大降低耗電。