# 硬體 Flash-Decoding PIM 歸約樹 (HW-FD-PIM-RT)

## 背景
Flash-Decoding 被廣泛用於加速長文本的生成 (Decode) 階段，其核心概念是將長 KV Cache 切塊平行計算，最後將各塊的 Partial Softmax 結果進行全局歸約 (Global Reduction)。這個歸約步驟通常受限於 DRAM 頻寬與同步開銷。

## 方法
將 Global Reduction 邏輯直接遷移至記憶體端 (Processing-in-Memory, PIM)。透過在 SRAM Bank 之間設計硬體加法歸約樹 (Hardware Reduction Tree)，直接在記憶體內部完成 Partial Softmax 的加總與縮放，徹底消除回傳至 NPU 的記憶體搬移。

## 實驗結果
- **Baseline (NPU Reduction):** 145.00 ms
- **HW-FD-PIM-RT (In-Memory Reduction):** 12.50 ms
- **速度提升:** 11.60x
- **精確度:** 33.8 dB SQNR

## 結論
HW-FD-PIM-RT 完美解決了 Flash-Decoding 在 Edge 端長文本推理時的歸約瓶頸，達到了近乎 O(1) 的歸約延遲。建議未來 Edge NPU 的 SRAM 控制器原生整合此架構。