# Hardware Flash-Decoding Reduction Fuser (HW-FDRF)

## 概述
在 Flash-Decoding 架構中，雖然能將 QK 計算分散至多個 Block，但最終仍需要將所有 Block 產生的 Partial States (包含 Softmax 最大值、分母與局部 Output) 從 SRAM 讀出，進行全局歸約 (Global Reduction) 才能得到最終結果。這會產生額外的記憶體頻寬開銷與延遲。

## 實驗方法
本研究提出整合硬體歸約樹 (Hardware Flash-Decoding Reduction Fuser, HW-FDRF)。利用晶片上的 Adder Tree，在各個 Block 運算單元產出 Partial States 時，即時 (On-the-fly) 在暫存器層級進行 Global Reduction，完全消除將 Partial States 寫入/讀出 SRAM 的需求。

## 實驗數據
*   **基準 SRAM 歸約延遲 (256 Blocks):** 0.0195 ms
*   **HW-FDRF 行內歸約延遲:** 0.000008 ms (8 cycles pipeline)
*   **延遲加速比 (Speedup):** 2441.41x

## 結論與架構建議
軟體層級的 Global Reduction 是一個受限於記憶體頻寬的操作。藉由 HW-FDRF 行內加法樹結構，我們可以將此階段的延遲降低三個數量級 (近乎零成本)，極大化長文本處理的效率。建議將此設計納入未來專精於超大 Context 的 Edge NPU 核心架構中。
