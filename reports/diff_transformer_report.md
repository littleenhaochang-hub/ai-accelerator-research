# Differential Transformer 硬體架構驗證報告

## 執行摘要
Differential Transformer (Diff Transformer) 透過計算兩個 Softmax 注意力矩陣的差值 ($Softmax(Q_1 K_1^T) - Softmax(Q_2 K_2^T)$) 來消除注意力雜訊 (Attention Noise)，使模型更專注於關鍵資訊。本實驗評估此雙重 Attention 架構對 Edge NPU 的算力與記憶體影響。

## 實驗數據與分析
- **目標架構**: 4K Context, 32 Heads (標準維度 128，Diff 架構切分為兩個 64 維度)
- **硬體效能比較**:
  - 標準 Attention MACs: 6.87e+10
  - Diff Attention MACs: 6.87e+10
  - 總 MACs 增長比: 1.00x (無額外負擔)
  - 差值運算 (Subtraction) 額外開銷: 5.37e+08 次操作

## 硬體架構結論
1. **運算量守恆**: 因為 Diff Transformer 將原本的 Head Dimension 切半 (例如 128 變成兩個 64)，所以 $Q \times K^T$ 的總乘加運算量 (MACs) 與標準 Transformer 完全相等，不會造成 Tensor Core 的額外負擔。
2. **潛在的 SRAM I/O 危機**: 如果軟體依序計算兩個 Attention Map 並寫回 SRAM，然後再讀出來相減，將會造成嚴重的記憶體頻寬浪費 (SRAM Thrashing)。
3. **協同設計提案**: 必須在 NPU 的 Softmax 引擎後端實作「Differential Softmax ALU (差分 Softmax 運算單元)」。將兩組半維度的 Attention 同時在 Register File 中算出 Softmax 後，直接在暫存器內執行硬體相減 (Zero-cycle Subtraction)，最後才將乾淨的差值寫回 SRAM，徹底避免中繼狀態的 I/O 懲罰。
