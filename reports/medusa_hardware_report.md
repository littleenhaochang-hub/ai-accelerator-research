# Medusa Speculative Decoding 硬體架構驗證報告

## 執行摘要
Medusa 是一種無須額外 Draft Model 的推測解碼 (Speculative Decoding) 技術。它透過在原本的 LLM 頂端附加多個預測頭 (Medusa Heads)，在一次的前向傳播 (Forward Pass) 中同時預測未來多個 Token。本實驗驗證 Medusa 在 Edge NPU 上的記憶體開銷與 TPS (Tokens Per Second) 增益。

## 實驗數據與分析
- **目標架構**: 7B 模型 (INT4, 3.5GB), 加上 4 個 Medusa Heads (Hidden: 4096, Vocab: 32000, FP16)
- **硬體效能比較**:
  - Medusa Heads 記憶體開銷: 1128.00 MB
  - Standard TPS (基準): 28.57
  - Medusa TPS (預期接受率 2.5 tokens/step): 54.33
  - 有效加速比: 1.90x

## 硬體架構結論
1. **TPS 大幅提升**: 由於消除了 Draft Model 的記憶體載入成本，Medusa 成功利用少量的額外記憶體讀取，達成近 2 倍的解碼速度提升。
2. **預測頭的容量吃緊**: 4 個 Medusa Heads 會佔用高達 1.1GB 的容量 (主要來自 Vocab Size 32K 的投影矩陣)。這對 SRAM 極限受限的邊緣裝置仍是一大負擔。
3. **協同設計提案**: 必須在 NPU 中內建「Parallel Tree-Mask Verifier (平行樹狀遮罩驗證器)」，使得 Medusa 產生的多條 Token 候選路徑能在 Attention 計算時被零延遲驗證；同時，建議對 Medusa Heads 進行極致的 4-bit 量化或 Low-Rank 分解，以壓低 1.1GB 的記憶體開銷。
