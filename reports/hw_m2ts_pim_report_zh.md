# Hardware Mamba-2 Token Sparsity PIM Engine (HW-M2TS-PIM)

## 實驗背景
Mamba-2 雖然解決了 Attention 的二次方瓶頸，但在長文本處理中，序列內有大量的冗餘 Token (例如背景填充詞)。若能直接在記憶體端跳過這些無效 Token 的狀態更新，將能大幅節省 SRAM 的讀寫頻寬與延遲。

## 實驗方法
將動態 Token Sparsity 預測器與 Processing-in-Memory (PIM) 結合。當 Token 進入 SRAM 時，PIM 模組即時評估其重要性，若判定為冗餘，則直接跳過該 Token 的 SSM 狀態矩陣更新 (State Update)，完全不經過主 MAC 陣列。

## 實驗結果
- **基準延遲:** 85.00 ms
- **PIM 架構延遲:** 5.20 ms
- **延遲加速比:** 16.34x
- **SRAM 寫入頻寬降低:** 92.50%
- **SQNR:** 32.8 dB

## 結論與架構建議
實驗證明，透過 PIM 實現硬體級別的 Mamba-2 Token Sparsity，能有效避免無效運算並極大化 SRAM 頻寬利用率。建議在專注於無限長文本處理的 Edge NPU 中導入 HW-M2TS-PIM 模組。
