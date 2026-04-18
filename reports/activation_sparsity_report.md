# Activation Sparsity (Zero-Skipping) 硬體加速驗證報告

## 執行摘要
在大型語言模型 (LLMs) 的 FFN (Feed-Forward Network) 層中，經過 ReLU 或 SwiGLU 激活函數後，通常存在極高的稀疏性 (Activation Sparsity，超過 60% 的值趨近於零)。本實驗驗證在硬體層面實作 Zero-Skipping (跳過零值乘加運算) 對算力與管線調度的影響。

## 實驗數據與分析
- **目標架構**: Llama 7B 等級 FFN (Hidden 4096, FFN 14336), 4096 Tokens
- **稀疏度**: 60%
- **算力比較**:
  - Dense MACs: 2.41e+11
  - Sparse MACs: 9.62e+10
  - 算力加速比: 2.50x
- **硬體開銷**: Bitmask (零值索引矩陣) 約 7.00 MB。

## 硬體架構結論
1. **潛在算力翻倍**: 成功跳過 60% 的無效運算，理想情況下可帶來 2.5 倍的 Down-Projection 吞吐量提升與顯著節能。
2. **管線氣泡問題 (Pipeline Bubbles)**: 雖然減少了 MACs，但動態的零值分佈會破壞 Tensor Core 陣列的規則執行步調，導致嚴重的硬體氣泡。
3. **協同設計提案**: 必須在 Edge NPU 的 MAC Array 前端實作「Asynchronous Zero-Skipping Controller (非同步零值跳過控制器)」與「Activation FIFO Buffer」。利用 Bitmask 提前預測零值並壓縮資料流，確保 Tensor Core 每個時脈週期都能獲得非零的有效操作數。
