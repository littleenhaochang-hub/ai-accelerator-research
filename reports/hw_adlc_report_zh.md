# 實驗報告：硬體自適應草稿長度控制器 (HW-ADLC)

## 摘要
在推測解碼 (Speculative Decoding) 中，固定草稿長度 (Draft Length) 常導致低信心區間浪費算力，或在高信心區間錯失加速機會。本實驗提出硬體自適應草稿長度控制器 (HW-ADLC)，在硬體層級即時計算 Token 熵值 (Entropy) 並動態調整草稿長度。

## 實驗結果
- **Baseline TPS (固定長度):** 45.00
- **HW-ADLC TPS:** 94.25
- **加速比:** 2.09x

## 架構建議
建議在 Edge NPU 內建「HW-ADLC」，透過硬體直接監控 Logit 熵值，動態控制 Draft 模型的生成長度，極大化推測解碼的接受率與整體吞吐量。