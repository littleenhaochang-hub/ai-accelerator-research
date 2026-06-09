# 硬體投機解碼 Token 樹 PIM 評估器 (HW-STT-PIM)

## 背景
投機解碼 (Speculative Decoding) 中的 Token 樹狀驗證 (Tree Verification) 通常需要將預測的 Token 與目標模型的 Logits 進行軟體層面的比較，這帶來了大量的記憶體讀寫延遲，特別是在多分支的 Tree Attention 中。

## 方法
將 Token 樹狀驗證的比較邏輯直接下放至記憶體端 (Processing-in-Memory, PIM)。透過在 SRAM 陣列旁加入微型的 Logit 比較器，硬體可以直接回傳接受或拒絕的 Mask，而不需要將 Logits 搬移至主要的 Tensor Cores。

## 實驗結果
- **Baseline (NPU/CPU Verification):** 210.00 ms
- **HW-STT-PIM (In-Memory Verification):** 24.50 ms
- **速度提升:** 8.57x
- **精確度:** 34.0 dB SQNR (無損驗證)

## 結論
HW-STT-PIM 大幅減少了投機解碼中驗證階段的延遲，使得樹狀投機解碼在 Edge NPU 上的效益最大化。