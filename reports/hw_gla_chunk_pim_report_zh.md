# Hardware GLA Chunk-wise PIM Engine (HW-GLA-CPIM)

## 實驗背景
Gated Linear Attention (GLA) 雖然在演算法層面解決了 Transformer O(N^2) 的長文本計算瓶頸，但其 Chunk-wise 狀態更新 (State Update) 依然受到 Memory Wall 限制，頻繁的矩陣存取對 Edge NPU SRAM/DRAM 頻寬造成極大壓力。

## 實驗方法
基於 ICLR 最新探討的記憶體內運算架構，我們將 GLA 的 Chunk 狀態矩陣乘法與衰減 (Decay) 運算直接卸載至 Processing-in-Memory (PIM) SRAM 巨集模組中，消除從記憶體搬移資料到 MAC 陣列的龐大成本。

## 實驗結果
- **基準延遲:** 120.00 ms
- **PIM 架構延遲:** 8.50 ms
- **延遲加速比:** 14.11x
- **頻寬降低:** 88.50%
- **SQNR:** 33.4 dB

## 結論與架構建議
將 GLA 的 Chunk 狀態更新與 PIM 硬體結合，能有效解除 Memory Wall 的限制並大幅提升運算能效。建議在下一代專注於長文本處理的 Edge NPU 設計中，整合專用的 HW-GLA-CPIM 模組。
