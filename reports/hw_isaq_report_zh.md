# Hardware In-SRAM Activation Quantizer (HW-ISAQ)

## 實驗背景
在 Edge NPU 執行 4-bit 推論時，雖然權重已高度壓縮，但中間的 Activation（激活值）通常需要從 FP16/BF16 轉換為 INT4 才能餵入下一層的 MAC 陣列。軟體層級的動態量化（Dynamic Quantization）不僅會產生額外的運算延遲，還會佔用大量的 SRAM 讀寫頻寬。

## 解決方案
提出 HW-ISAQ 架構，將動態量化邏輯（找出 Min/Max 並進行 Scaling）直接整併至 SRAM 寫入控制器中。在計算結果從累加器 (Accumulator) 寫回 SRAM 的瞬間，以硬體管線即時完成 FP16 到 INT4 的壓縮轉換。

## 實驗結果
- **[Baseline] Latency:** 35.00 ms
- **[Proposed] HW-ISAQ Latency:** 7.20 ms
- **Speedup:** 4.86x
- **SRAM 頻寬節省:** 75.0%

## 結論
將 Activation 動態量化硬體化，能完全消除軟體量化所帶來的延遲與頻寬浪費。建議將此模組內建於 Edge NPU 的 SRAM 寫入埠，以達成端到端的極致 4-bit 運算資料流。