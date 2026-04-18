# FP6 (E3M2) Quantization 硬體架構驗證報告

## 執行摘要
在 LLM 模型量化中，FP6 (6-bit 浮點數，例如 E3M2) 被認為是精度 (SQNR 幾乎等同 FP16) 與模型大小之間的完美平衡，特別是在 INT4 精度不足而 FP8 壓縮率不夠的場景下。本實驗驗證 FP6 在實際硬體 (Edge NPU) 上的記憶體對齊 (Memory Alignment) 與解壓縮開銷。

## 實驗數據與分析
- **目標架構**: 6B 參數模型 (FP16: 12GB -> FP6: 4.5GB -> INT4: 3.0GB)
- **硬體效能評估**:
  - 記憶體匯流排 (256-bit): 單次傳輸可塞入 42 個 FP6 數值，浪費 4 bits (頻寬浪費率 1.56%)。
  - SRAM 讀取對齊懲罰: 極高。6-bit 無法被 8 (Byte) 整除，導致硬體 DMA 控制器需要實作非對齊的位元平移 (Bit-shifting) 與遮罩 (Masking) 邏輯。
  - 解碼器 (Dequantizer) 面積: 可使用微型 64-entry LUT (128 Bytes)，開銷極低。

## 硬體架構結論
1. **致命的記憶體非對齊 (Unaligned Access)**: FP6 最大的硬傷不是算力，而是其 6-bit 寬度會破壞現代電腦體系結構中基於 Byte (8-bit) 與 Word (32/64-bit) 的記憶體定址與傳輸邊界。
2. **協同設計提案**: 必須在編譯階段 (Software Compiler) 與 NPU DMA 控制器實作「24-bit/192-bit 封裝協定 (Packing Protocol)」。將 4 個 FP6 打包成 24-bit，或將 32 個 FP6 打包成 192-bit (3x 64-bit word)，然後在 SRAM 讀取埠直連一個「Bit-Unpacking Engine」，負責即時拆解並送入 64-entry LUT 進行零延遲的 FP16/FP8 還原。
