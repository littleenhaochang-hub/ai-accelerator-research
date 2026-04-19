# YOCO (You Only Cache Once) 硬體架構驗證報告

## 執行摘要
為解決超長文本推論的記憶體牆問題，微軟提出的 YOCO (You Only Cache Once) 架構將 Transformer 分為底層的 Self-Decoder 與頂層的 Cross-Decoder。頂層網路不再生成與儲存專屬的 KV Cache，而是重複利用底層的全域 KV Cache。本實驗驗證其在硬體層面的 SRAM 佔用與頻寬釋放效能。

## 實驗數據與分析
- **目標架構**: 32K Context, 32 Layers, 32 Heads, 128 Dim (FP16)
- **硬體效能評估**:
  - 標準 KV Cache 佔用: 16384.00 MB (16GB)
  - YOCO KV Cache 佔用: 8192.00 MB (8GB)
  - 記憶體容量需求縮減: 2.00x (節省 50%)
  - SRAM 取讀延遲: 由 8000.00 us 下降至 4000.00 us。

## 硬體架構結論
1. **直接腰斬 KV Cache 開銷**: 透過演算法層面的解耦，YOCO 成功讓 32K 長文本的推論記憶體需求減半，大幅降低 DRAM 溢出 (Spilling) 的機率。
2. **頂層零記憶體讀取**: Cross-Decoder (頂層網路) 讀取的是完全相同的 Global KV Cache。如果硬體設計得當，這些資料可以被「釘住 (Pinned)」在 SRAM 中，免除重複從 DRAM 讀取的耗損。
3. **協同設計提案**: 為了最大化 YOCO 的優勢，Edge NPU 應該實作一組「SRAM Broadcast Bus (靜態 SRAM 廣播匯流排)」。在執行 Cross-Decoder 運算時，硬體不再發出 KV Read Request，而是直接將 Pin 在 SRAM 內的 Global KV 透過廣播匯流排同時餵給所有的 Tensor Core ALUs，達成頂層網路 Zero-Memory-Fetch 的極致效能。
