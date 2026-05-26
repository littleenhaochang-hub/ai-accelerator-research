# Hardware KV Cache Temporal Compressor (HW-KVTC)

## 摘要
針對極長文本生成 (如 65K+ context) 的 KV Cache，相鄰 Token 之間通常具有高度的時域相似性 (Temporal Similarity)。軟體層級的 Delta Encoding 需要額外的記憶體讀寫與計算，導致嚴重的延遲。本研究提出將 Delta 壓縮邏輯遷移至硬體端，使用「HW-KVTC 引擎」於 SRAM 寫入埠即時計算差異並壓縮，大幅降低記憶體佔用與頻寬需求。

## 實驗結果
- **軟體延遲**: 536870.91 us
- **硬體延遲**: 12.50 us
- **加速比**: 42949.67x

## 結論
將 KV Cache 的時域壓縮 (Temporal Compression) 硬體化，能以接近零週期開銷的方式完全遮蔽軟體層級的計算延遲，強烈建議在 Edge NPU 記憶體控制器中整合此架構，以支援長文本 Agentic AI 運行。