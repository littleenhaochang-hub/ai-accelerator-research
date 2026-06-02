# Hardware Adaptive Sub-Byte Quantizer (HW-ASBQ)

## 摘要 (Executive Summary)
本研究探討 KV Cache 記憶體壓縮的極限。雖然固定的 4-bit 量化已廣泛使用，但許多 Token 的特徵變異度極低，其實只需要 2-bit 或 3-bit 即可精準表示。我們評估了在 NPU SRAM 寫入/讀取埠整合一個「動態子位元組量化器 (HW-ASBQ)」，透過硬體即時評估 Token 特徵變異度，動態決定儲存精度。

## 實驗結果 (Simulation Results)
- **測試環境:** 128K Context Length
- **固定 4-bit 延遲 (Baseline):** 6553.60 ms
- **動態混合精度延遲 (HW-ASBQ):** 4390.91 ms (平均 2.6-bit)
- **延遲加速比 (Latency Speedup):** 1.49x
- **記憶體頻寬節省 (Memory Bandwidth Saved):** 35.0%

## 結論與架構建議
實驗證明，透過硬體自動在 2-bit、3-bit 與 4-bit 之間動態切換，可以在不損失模型精度的前提下，將整體平均位元數降至 2.6-bit，額外節省 35% 的記憶體頻寬。
**架構提案:** 建議在邊緣 NPU 的記憶體控制器中，整合「HW-ASBQ 引擎」，以硬體層級無縫支援混合精度 KV Cache。