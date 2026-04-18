# SmoothQuant 硬體架構驗證報告

## 執行摘要
在大模型 (LLM) 推論中，Activation (激活值) 經常出現極端的 Outliers (異常值)，導致單純的 INT8 或 INT4 量化發生嚴重的精度坍塌。SmoothQuant 透過數學轉換 $Y = (X \cdot S^{-1}) \cdot (S \cdot W)$，將量化難度從激活值轉移到權重上。本實驗驗證此演算法在硬體實作上的運算與記憶體開銷。

## 實驗數據與分析
- **目標架構**: 8B 模型 (Hidden Dim 4096, 32 Layers), Context 4096
- **硬體效能評估**:
  - 縮放因子 (Scaling Vectors) 記憶體開銷: 僅 0.25 MB (全網路總和)
  - 基線 MACs (Dense): 2.20e+12
  - 平滑化額外 MACs (Smoothing): 5.37e+08
  - 算力額外開銷比率: 0.0244%

## 硬體架構結論
1. **極低的硬體開銷**: SmoothQuant 的縮放運算 (O(N)) 相對於矩陣乘法 (O(N^2)) 而言，算力佔比不到 0.03%，且額外記憶體佔用極小 (0.25MB)，完全可以直接存放在 Edge NPU 的 SRAM 中。
2. **協同設計提案**: 為了實現零延遲的 Outlier 平滑化，必須在 Tensor Core (MAC 陣列) 的輸入端實作一個專屬的「Vector Scaling Unit (向量縮放單元)」。當激活值從 SRAM 讀出時，即時與 $S^{-1}$ 進行 element-wise 乘法，然後再送入 INT8/INT4 MACs，如此即可在不損失 TPS 的情況下維持模型高精度。
