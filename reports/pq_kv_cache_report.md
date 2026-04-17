# Product Quantization KV Cache Hardware Analysis

## 實驗背景
由於硬體記憶體頻寬成為長文本推理的主要瓶頸，我們針對 KV Cache 提出了基於 Product Quantization (PQ) 的壓縮架構驗證。目標是大幅度降低 KV 緩存的記憶體佔用。

## 實驗方法
透過 Python/NumPy 撰寫了 `product_quantization_kv_sim.py`，模擬將 4096 維度的 KV 向量切割為 32 個 Subvectors，並使用大小為 256 的 Codebook 進行索引。

## 實驗數據
- **Baseline Memory (16K tokens)**: 134.22 MB
- **PQ Compressed Memory**: 2.62 MB
- **Memory Footprint Reduction**: 98.05%
- **Effective Bandwidth Speedup**: 0.25x (瓶頸轉移至 LUT 查詢延遲)

## 硬體架構結論
PQ 雖然能減少 98% 的記憶體佔用，但如果單純在軟體中進行 LUT 查詢還原，反而會造成效能倒退（約 0.25 倍速度）。因此，必須在 Edge NPU 內整合專用的「SRAM LUT Array」，讓 PQ 的索引解壓縮能夠 On-the-fly 執行，隱藏延遲，才能真正達成高達 50 倍的理論記憶體頻寬提升。
