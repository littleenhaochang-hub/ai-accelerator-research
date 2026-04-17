# W4A4 FFN 激勵異常值 (Activation Outlier) 實驗報告

## 1. 實驗背景
在推進邊緣設備 (如 Mac mini) 的純 INT4/FP4 運算時，我們發現 FFN 層存在極端的 Activation Outliers (少數 Channel 的數值是一般的幾十倍)。若直接進行 4-bit 量化，這些 Outliers 會撐大量化的 Range，導致其餘 99% 的一般特徵被壓縮為 0，嚴重損害模型準確度 (Cosine Similarity < 90%)。

## 2. 探勘文獻方法
根據最新 arXiv 與 ICML 論文，主流的硬體協同設計解法包括：
1. **Hadamard Rotation / ConvRot:** 透過正交矩陣旋轉來平均化 Channel 之間的變異數。
2. **Scale Folding (RAMP):** 在 Runtime 之前，將 Activation 的極端尺度乘數移轉至 Weight 中，使得實際的 Activation 分佈變得平滑。

## 3. Prototype 驗證與數據
我們以 Python 撰寫了輕量級的 Scale Folding 模擬腳本 (`w4a4_outlier_sim.py`)。
設定：產生 4096 維度，其中包含 1% 高達 80 的異常值。

**實驗結果：**
- 原始最大值 77.79 -> 導致 Quantization Step 高達 5.19
- 平滑化 (Scale Folding) 後最大值 5.00 -> Quantization Step 縮減至 0.33
- 精度提升倍率: 15.6x
- 演算法延遲: 0.23 ms

**結論：**
Scale Folding 在極低延遲下將量化解析度提升了 15 倍。在實際硬體架構上，這代表我們不需為了少數 Outliers 引入混合精度 (Mixed Precision) MAC 單元，全陣列均可採用高能效的 INT4/FP4 乘加器，從而極大化 Compute-Bound 效能。
