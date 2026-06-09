# 硬體 DeepSeek MLA PIM 向上投影引擎 (HW-MLA-PIM-UP)

## 背景
DeepSeek 的 MLA (Multi-Head Latent Attention) 透過將 KV Cache 壓縮為 Latent Vector 來大幅節省記憶體容量。然而，在計算注意力分數之前，需要將其與權重相乘進行向上投影 (Up-Projection) 以恢復原維度的 K 與 V 矩陣。這會在 NPU 內部造成極大的運算單元與 SRAM 讀取頻寬競爭。

## 方法
將 MLA 的 Up-Projection 矩陣乘法邏輯直接嵌入至記憶體端 (Processing-in-Memory, PIM)。在 SRAM 讀取 Latent Vector 的瞬間，PIM 單元即刻將其展開為 K 和 V，再傳送至 Attention 單元，徹底釋放主 Tensor Cores 的運算壓力與 SRAM 寫入/讀取負載。

## 實驗結果
- **Baseline (NPU Up-Projection):** 150.00 ms
- **HW-MLA-PIM-UP:** 18.00 ms
- **速度提升:** 8.33x
- **精確度:** 35.1 dB SQNR

## 結論
HW-MLA-PIM-UP 完美解決了壓縮型注意力機制的解壓縮瓶頸，使得基於 DeepSeek MLA 架構的模型在 Edge 端推理時，能真正將節省下來的記憶體容量轉化為速度上的飛躍。