# Gated Linear Attention (GLA) 硬體架構驗證報告

## 執行摘要
傳統的 Softmax Attention 會產生隨文本長度 $O(N)$ 線性增長的 KV Cache，這在超長文本 (Long-Context) 邊緣推論時會引發嚴重的記憶體耗盡 (OOM) 問題。Gated Linear Attention (GLA) 作為 RNN / 線性注意力的變形，將歷史資訊壓縮到固定大小的隱藏狀態 (Fixed-size Hidden State) 中，並透過 Associative Scans 解決平行化訓練問題。本實驗驗證 GLA 應用於 Edge NPU 時的記憶體與算力表現。

## 實驗數據與分析
- **目標架構**: 8K Context, 32 Heads, 128 Dim
- **硬體效能比較**:
  - Softmax Attention KV Cache 容量: 128.00 MB
  - GLA 固定狀態 (State Matrix) 容量: 1.00 MB
  - 記憶體縮減比率: 128.00x
  - 單個 Token 生成算力 (N=8192):
    - Softmax MACs: 6.71e+07
    - GLA MACs: 1.05e+06 (不隨 N 增長)
  - 算力加速比: 64.00x

## 硬體架構結論
1. **打破長文本記憶體牆**: GLA 成功消滅了動態增長的 KV Cache，並將 8K 上下文的記憶體足跡從 128MB 壓縮至區區 1MB，這對 SRAM 極度受限的 Edge NPU 是革命性的進步。
2. **$O(1)$ 的生成複雜度**: 推論生成時，算力開銷與文本長度完全無關，帶來了 64 倍的極端加速。
3. **協同設計提案**: GLA 的核心瓶頸在於 Prefix 階段的 Associative Scan。建議在 NPU 中內建專屬的「Associative Scan ALUs (結合律掃描運算單元)」，以硬體層次執行 element-wise 的資料相依運算，取代傳統針對矩陣乘法優化的 Tensor Core，以發揮 GLA 的最大硬體潛力。
