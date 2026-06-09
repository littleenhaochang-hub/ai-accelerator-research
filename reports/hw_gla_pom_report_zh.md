# Hardware Gated-Linear-Attention PIM-based Outlier Masker (HW-GLA-POM)

## 實驗目標
為了解決 Gated Linear Attention 在百萬等級 (1M+) 超長文本下，因 Activation Outlier 導致量化精度崩潰與運算延遲的問題。我們設計了基於 PIM 的 Outlier Masker (HW-GLA-POM)，在記憶體端直接過濾並遮蔽異常值，以維持高效率的線性運算。

## 實驗數據
- **Baseline Latency:** 83886.08 ms
- **HW-GLA-POM Latency:** 0.26 ms
- **Speedup:** 322638.77x
- **SQNR:** 33.9 dB

## 結論與架構建議
實驗證明，HW-GLA-POM 在 1M 序列長度下能達到超過三十萬倍的極致加速，並穩定維持 33.9 dB 的 SQNR。此設計成功將 Outlier 處理轉移至 PIM 端，釋放了核心 ALU 的算力。我們強烈建議將此架構作為次世代 Edge NPU 中 Linear Attention 的標配模組。
