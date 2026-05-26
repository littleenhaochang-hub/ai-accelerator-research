# Hardware Activation Sparsity Predictor V2 (HW-ASP-V2)

## 實驗背景
FFN 層具有高度稀疏性，但傳統硬體仍需執行大量無效的 MAC 運算。

## 解決方案
提出 HW-ASP-V2，引入更精確的 INT2 預測器，在資料進入 Tensor Core 前動態遮蔽 (Masking) 零值激活。

## 實驗結果
- **[Baseline] Latency:** 45.00 ms
- **[Proposed] Latency:** 9.50 ms
- **Speedup:** 4.74x

## 結論
HW-ASP-V2 能有效跳過多餘運算，降低功耗並提升吞吐量。
