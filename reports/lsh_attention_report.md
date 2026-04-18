# LSH Attention (Locality Sensitive Hashing) 硬體加速驗證報告

## 執行摘要
在處理 32K 等長文本推論時，傳統 Attention 的 O(N^2) 複雜度會成為嚴重的算力與記憶體瓶頸。本實驗探討 LSH Attention (如 Reformer) 在硬體上的執行效益與潛在的記憶體存取問題。

## 實驗數據與分析
- **目標架構**: 32K Context, 4 Hashes, 128 Buckets
- **總運算量比較**:
  - Baseline O(N^2) MACs: 1.07e+09
  - LSH Attention MACs: 5.03e+07 (包含 Hash 投影與 Bucket 內 Attention)
  - 算力加速比: 21.33x

## 硬體架構結論
1. **極致的算力節約**: LSH 成功將 32K 文本的 Attention 運算量減少了超過 95% (加速比高達 21 倍)。
2. **記憶體局部性破壞 (Memory Locality Destruction)**: 雖然算力大幅下降，但 LSH 將 token 打散到不同的 bucket，導致記憶體存取變成高度隨機 (Random Access)，嚴重破壞 SRAM 與 DRAM 的局部性 (Spatial Locality)，可能造成嚴重的頻寬浪費與管線停滯 (Pipeline Stalls)。
3. **協同設計提案**: 若要將 LSH 引入 Edge NPU，必須實作專用的「Hardware Scatter/Gather Engine (硬體散佈/聚合引擎)」，允許硬體在搬移資料時動態重組記憶體佈局 (Memory Coalescing)，以恢復記憶體頻寬的使用率。
