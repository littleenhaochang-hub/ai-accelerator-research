# Token Merging (ToMe) 硬體加速驗證報告

## 執行摘要
在 Transformer 架構 (特別是 ViT 與長文本 LLM) 中，隨著深度增加，許多 token 乘載的語義會趨於一致。本實驗驗證了 Token Merging (ToMe) 演算法在硬體層面的效益，透過在每一層逐步合併相似度高的 token，以減少後續層的 Attention O(N^2) 運算負載。

## 實驗數據與分析
- **目標架構**: 32層 Transformer, 初始 4096 tokens, 每層合併 64 個 tokens
- **總運算量比較**:
  - Baseline MACs: 4.40e+12
  - ToMe MACs: 2.62e+12
  - 算力加速比: 1.68x
  - 最終層 Token 數量: 2048

## 硬體架構結論
1. **運算量與能耗雙降**: 藉由減少 token 數量，ToMe 成功將整體 Attention 運算負載降低了約 40% (加速比 1.68 倍)，大幅緩解後段網路的記憶體頻寬與算力瓶頸。
2. **硬體/軟體協同設計提案**: ToMe 的核心瓶頸在於尋找相似 token 所需的 Bipartite Matching (通常依賴 Cosine Similarity)。由於軟體執行這些 O(N^2) 距離計算會抵銷合併帶來的加速，提案在 Edge NPU 內建「Hardware Bipartite Matching Engine (硬體二分匹配引擎)」，專門處理向量內積與排序，達成 Zero-overhead token 聚合。
