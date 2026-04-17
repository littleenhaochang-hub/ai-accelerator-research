# OCP Microscaling Formats (MX4) Hardware Analysis

## 實驗背景
隨著模型規模擴張，標準的 FP8 已經逐漸面臨記憶體頻寬的極限，而傳統的 INT4 則因為 Outlier 導致動態範圍 (Dynamic Range) 嚴重不足，引發精度崩潰。我們探討基於 OCP (Open Compute Project) 規範的 Microscaling Formats (MX4)，將一組資料共用一個 Shared Exponent，以評估其硬體實作的 PPA 效益。

## 實驗方法
撰寫 `mx4_microscaling_sim.py`，模擬 4096 x 4096 矩陣在 Block Size 為 32 下的記憶體佔用與頻寬延遲，並分析所需的硬體支援。

## 實驗數據
- **Baseline (FP16) Memory**: 33.55 MB
- **MX4 (4-bit data + 8-bit shared scale) Memory**: 8.91 MB
- **Memory Footprint Reduction**: 73.44%
- **Effective Bandwidth Speedup**: 3.76x
- **Dynamic Range Maintained**: ~48.2 dB (透過 8-bit shared scale 保持高動態範圍)

## 硬體架構結論
MX4 在維持接近 FP16/FP8 的動態範圍下，能實現 3.76 倍的記憶體頻寬提升。
為了支援此架構，我們必須在 Edge NPU 的 MAC Array (乘加陣列) 之前整合專用的 **Shared-Exponent Aligner (共用指數對齊器)**。該單元需要能以 Block 為單位 (如 32 elements) 即時將 4-bit Mantissa 進行位移對齊 (Shifting)，從而確保在無 pipeline stalling 的情況下完成微縮放計算。這將成為下一代 NPU 的標準配置。
