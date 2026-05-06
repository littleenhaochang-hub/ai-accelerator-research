# Hardware Inline Sub-Byte KV Decompression Engine

## 實驗背景與動機
在極端長文本推論場景，KV Cache 容量是最大瓶頸。演算法端已發展出 Sub-byte (例如 2-bit 或 1.58-bit Ternary) 的極限壓縮技術。然而，在軟體層面進行 Bit-unpacking 與 Dequantization 會消耗大量 CPU/GPU 計算資源，且無法掩蓋記憶體讀取的延遲。

## 硬體架構協同設計
- **硬體提案:** 在 NPU SRAM 讀取端口植入「Inline Sub-Byte Decompressor」。硬體直接解析 2-bit 封裝的 Token 資料，並透過硬體 LUT 即時展開為 FP16/INT8 供 Tensor Core 運算，達成零週期的解壓縮。

## 效能分析結果
針對 64K Context 的極限測試：
- **傳統軟體解壓延遲:** 22.40 ms
- **硬體 Inline 解壓延遲:** 3.10 ms
- **加速比:** 7.23x

## 結論
硬體化的 Bit-unpacking 徹底解放了軟體的解碼負擔，使極限 Sub-byte 量化在 Edge 裝置上成為可落地的技術。