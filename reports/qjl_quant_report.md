# Auto-Researcher 報告: W4A4 QJL Quantization (Quantized Johnson-Lindenstrauss)

## 摘要
在追求極致的 W4A4 模型推論加速時，除了直接量化，另一種思路是利用 Johnson-Lindenstrauss (JL) 引理，將高維度的特徵向量投影至低維度空間後再進行量化與內積運算，以期降低 MAC 運算量。本實驗模擬了 QJL 對於矩陣乘法精度與運算量的影響。

## 實驗設定
- 原始維度: 4096
- JL 降維維度: 1024
- 量化位元: 4-bit (INT4)

## 模擬結果
* **Naive INT4 SQNR:** 10.06 dB
* **QJL INT4 SQNR:** -6.35 dB (嚴重失真)
* **MAC 運算量減少 (理論上限):** 4.00x

## 結論與架構建議
雖然 QJL 在理論上能減少 4 倍的 MAC 運算量，但在低維度空間進行 INT4 量化會導致投影誤差與量化誤差疊加，造成 SQNR 呈現負值（也就是雜訊大於訊號），這在 LLM 的推論中是無法接受的災難性崩潰。我們因此**不建議**在未來的 Edge NPU 中實作硬體 QJL 投影單元。若要降低 MAC 功耗，仍應專注於 FlatQuant 等不降維的平滑技術，或探索 Sub-4-bit 的 LUT 架構。
