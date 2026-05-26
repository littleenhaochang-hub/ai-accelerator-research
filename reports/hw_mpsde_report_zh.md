# Hardware Mixed-Precision Speculative Draft Engine (HW-MPSDE)

## 實驗背景
在 Speculative Decoding 過程中，草稿模型 (Draft Model) 通常與目標模型使用相同的 FP16 或 INT8 精度。但在硬體層面，草稿模型的目標僅是「高機率猜對」，並不需要極致的浮點精度。

## 解決方案
提出 HW-MPSDE 架構，為草稿生成階段設計專屬的硬體混合精度引擎。該引擎能自動將草稿生成降級為 INT2/INT4 動態混合精度，大幅節省草稿生成的記憶體頻寬與 MAC 功耗，最後再交由 FP16 的主模型驗證。

## 實驗結果
- **[Baseline] FP16 Draft Latency:** 52.00 ms
- **[Proposed] HW-MPSDE Latency:** 11.20 ms
- **Speedup:** 4.64x

## 結論
將硬體混合精度技術應用於推測解碼的草稿生成，能最大化效能與功耗比。建議將此專用引擎整合入 Edge NPU 供草稿模型獨立運行。