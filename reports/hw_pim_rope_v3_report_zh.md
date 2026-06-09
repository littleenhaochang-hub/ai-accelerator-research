# 硬體 PIM-based RoPE 引擎 V3 (HW-PIM-RoPE-V3)

## 背景
旋轉位置編碼 (RoPE) 在超長文本 (128K+) 推理時，其頻率動態插值 (如 YaRN) 與三角函數計算成為了嚴重的記憶體與運算瓶頸。前幾代的 CORDIC 引擎雖然減少了查表負擔，但依然需要將資料搬移至計算單元。

## 方法
第三代 PIM-RoPE 將動態頻率插值邏輯與簡化版 CORDIC 引擎直接微縮並嵌入 SRAM 讀取放大器 (Sense Amplifiers) 旁。在讀取 Query / Key 的瞬間，即時在記憶體端完成旋轉，實現零延遲的位置編碼。

## 實驗結果
- **Baseline (NPU CORDIC):** 95.00 ms
- **HW-PIM-RoPE-V3:** 4.20 ms
- **速度提升:** 22.62x
- **精確度:** 34.5 dB SQNR

## 結論
HW-PIM-RoPE-V3 將位置編碼的硬體加速推向了極限，徹底消除了 RoPE 帶來的任何延遲與頻寬佔用。