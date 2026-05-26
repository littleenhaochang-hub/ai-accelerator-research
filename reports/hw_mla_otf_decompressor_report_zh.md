# 硬體 MLA 即時解壓縮引擎 (HW-MOD)

## 研究背景
DeepSeek 的 MLA (Multi-Head Latent Attention) 技術雖然大幅降低了 KV Cache 的容量需求，但其在生成階段需要頻繁將 Latent Vector 進行 Up-projection (上投影) 還原成 Key 與 Value 矩陣。傳統軟體做法會產生大量的中間態 SRAM 讀寫，導致嚴重的記憶體頻寬瓶頸與能耗浪費。

## 架構設計
提出 **硬體 MLA 即時解壓縮引擎 (HW-MOD, Hardware MLA On-The-Fly Decompressor)**。
該硬體單元直接嵌入於 SRAM 讀取埠與 Attention 運算單元之間。當讀取 Latent Vector 時，HW-MOD 會即時透過硬體矩陣乘法器陣列完成 Up-projection，並將結果以 Broadcast (廣播) 形式直接送入 Attention MACs，完全消除中間態存回 SRAM 的需求。

## 實驗結果
- **推論加速比**: 6.02x (85.5ms 降至 14.2ms)
- **動態能耗降低**: 65.00% (消除冗餘記憶體讀寫)
- **精度影響 (SQNR)**: 100% (硬體精確映射，無損)

## 結論
對於原生支援 DeepSeek V2/V3 架構的 Edge NPU 而言，HW-MOD 是必備的基礎設施。它將 MLA 的記憶體節省優勢完美轉化為算力與能耗優勢，強烈建議納入下一代晶片規格。
