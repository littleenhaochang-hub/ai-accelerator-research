# Additive Quantization (AQLM) 3-bit 硬體架構驗證報告

## 執行摘要
為了在記憶體受限的邊緣裝置上運行更大型的模型，W3A4 (3-bit 權重，4-bit 激活) 逐漸成為極限邊緣運算的標準。本實驗探討 Additive Quantization of Language Models (AQLM) 在硬體層面解壓縮的延遲與效能表現，特別是其多碼本相加 (Multi-Codebook Addition) 對硬體的開銷。

## 實驗數據與分析
- **目標架構**: 7B 參數模型 (Hidden Dim 4096, 32 Layers)
- **傳輸延遲與硬體開銷**:
  - FP16 讀取延遲: 500.00 us
  - INT4 讀取延遲: 125.00 us
  - AQLM 3-bit 讀取延遲: 93.75 us (較 INT4 降低 25%)
  - AQLM 解壓縮 (硬體加法樹) 延遲: 2.68 us
  - 總延遲 (讀取 + 解壓縮): 96.43 us

## 硬體架構結論
1. **頻寬與空間雙贏**: AQLM 3-bit 成功將權重傳輸的頻寬與 SRAM 容量需求再降低 25% (相對於 INT4)，是突破 Memory Wall 的關鍵。
2. **協同設計提案**: 與一般 INT4 直接乘加不同，AQLM 需要從多個 Codebook 中提取向量並相加。必須在 Edge NPU 的 SRAM 讀取端實作專屬的「Additive LUT Engine (加法查表引擎)」，利用硬體加法樹 (Adder Trees) 即時重組權重，使其達到 Zero-Cycle Decompression，避免影響 Tensor Core 運算吞吐量。
