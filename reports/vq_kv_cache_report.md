# Vector Quantization (VQ) KV Cache 硬體架構驗證報告

## 執行摘要
在處理 32K 超長文本 (Long-Context) 推論時，FP16 KV Cache 會消耗高達 4GB 的 SRAM，導致 Edge NPU 容量耗盡 (OOM)。本實驗探討 Vector Quantization (向量量化, VQ) 取代純量量化 (Scalar Quantization) 對硬體頻寬與延遲的影響。

## 實驗數據與分析
- **目標架構**: 32K Context, 8 Heads, 128 Dim, 32 Layers
- **壓縮比例**: Block Size = 4, 8-bit Codebook (壓縮比 8x)
- **硬體效能數據**:
  - FP16 KV 佔用空間: 4096.00 MB
  - VQ KV 佔用空間: 512.00 MB (8.0x reduction)
  - FP16 SRAM 讀取延遲: 2000.00 us
  - VQ (含 LUT 解碼 overhead) 總延遲: 786.87 us

## 硬體架構結論
1. **SRAM 空間與頻寬釋放**: VQ 成功將 KV Cache 容量減少 87.5%，並將總傳輸延遲縮減。
2. **解碼瓶頸 (Decoding Overhead)**: 雖然讀取變快，但查表 (Look-Up Table, LUT) 會帶來額外延遲 (約佔總延遲的 68%)。
3. **協同設計提案**: Edge NPU 必須內建專用的「SRAM Codebook Decoder Arrays」，使其與 Tensor Cores 平行運作。當從 SRAM 取出 8-bit index 時，直接透過微型 Codebook SRAM 展開為 4 組 FP16/INT4 數值，達成 Zero-cycle dequantization。
