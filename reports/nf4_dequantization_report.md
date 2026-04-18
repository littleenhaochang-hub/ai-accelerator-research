# NormalFloat4 (NF4) Dequantization 硬體架構驗證報告

## 執行摘要
在執行高精度的邊緣推論時，NF4 (NormalFloat4) 由於其非線性分佈的特性，能夠在 4-bit 量化下提供優於 INT4 的 SQNR (訊號雜訊比)。本實驗驗證了 NF4 量化權重對記憶體頻寬的貢獻，以及非線性查表解量化 (LUT Dequantization) 造成的硬體負載。

## 實驗數據與分析
- **目標模型**: 7B 等級 LLM (Hidden Dim: 4096, 32 Layers)
- **傳輸延遲比較**:
  - FP16 Weight 讀取延遲: 500.00 us
  - NF4 Weight 讀取延遲: 125.00 us (縮減 75%)
  - NF4 LUT 解碼延遲 (軟體/離散硬體估算): 5.37 us
  - 總 NF4 推論延遲 (讀取 + 解碼): 130.37 us

## 硬體架構結論
1. **傳輸頻寬大幅釋放**: 4-bit 的 NF4 成功將 SRAM 傳輸延遲與頻寬消耗降低 4 倍。
2. **查表運算為潛在瓶頸**: NF4 不是簡單的位移或線性乘加，它強烈依賴 16-entry 的非線性查表 (LUT)。若在 ALUs 內部解碼會佔用額外的暫存器與時脈週期。
3. **協同設計提案**: 必須在 Edge NPU 的 SRAM 讀取埠口 (Read Ports) 直連「Fused NF4 SRAM Decompressor (融合式 NF4 解壓縮器)」。透過直接在實體層面硬體查表，將讀取的 4-bit 訊號在 0 cycle 內轉譯為 FP16 餵給 Tensor Core，達到完全的運算/傳輸重疊。
