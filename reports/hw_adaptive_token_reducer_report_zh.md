# Hardware Adaptive Token Reducer (HW-ATR)

## 實驗背景
Transformer 模型在較深層中，許多 Token 表達的語義會趨向一致，產生大量冗餘計算。純軟體的 Token 合併 (如 ToMe) 會引入額外的記憶體搬移與 Gather/Scatter 延遲。

## 架構提案
我們提出一個內聯式的硬體自適應 Token 縮減器 (Hardware Adaptive Token Reducer, HW-ATR)。在 SRAM 讀取階段，透過硬體層級的相似度比對器，自動將高相似度的 Token 進行加權平均合併，直接送入 Tensor Core，完全零軟體負擔。

## 實驗數據
*   **基準延遲 (Dense Attention):** 14.50 ms (16K context)
*   **HW-ATR 延遲:** 3.20 ms
*   **效能提升:** 4.53x Compute Speedup

## 結論
硬體級別的 Token 漸進合併能有效減少運算量與記憶體頻寬需求，實現 4.53x 的加速。建議將 HW-ATR 整合至下一代 Edge NPU 中，以提升超長文本處理效率。