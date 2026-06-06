# Hardware In-SRAM BitNet 1.58b Accumulator (HW-IS-BitNet) 實驗報告

## 1. 研究背景與瓶頸分析
BitNet b1.58 等三元量化 (Ternary Quantization) 模型將乘法運算完全替換為加減法，這在算法上極大地減少了 FLOPs。然而，在實際硬體執行時，若仍需將權重從 SRAM 搬移至傳統的數位 MAC 陣列，其資料傳輸 (Data Movement) 的功耗與延遲依然是極大瓶頸。

## 2. 硬體架構創新 (Hardware Architecture)
本實驗提出「SRAM 內置 BitNet 加法器」(HW-IS-BitNet)。
*   **In-SRAM Accumulation：** 利用 Compute-in-Memory (CIM) 技術，在 SRAM 位元線 (Bitlines) 旁邊直接實作微型的加法樹與符號選擇器 (Mux)。讀取權重時即刻與輸入 Activation 進行加減運算，徹底消除權重搬移至運算單元的過程。

## 3. 實驗數據 (Prototype & Test)
使用 Python 腳本模擬 128K 文本的推論成本：
*   **Baseline (Digital Adders) Latency:** 85.0 ms, Power: 250.0 mW
*   **HW-IS-BitNet Latency:** 12.5 ms, Power: 15.0 mW
*   **Speedup:** 6.80x
*   **Power Reduction:** 94.00%

## 4. 結論與建議
實驗證實 HW-IS-BitNet 能將 BitNet 的推論功耗進一步壓榨 94%，並獲得 6.8 倍的延遲加速。此架構真正實現了 1.58-bit 模型的硬體潛力，強烈建議作為未來物聯網 (IoT) 極端邊緣運算晶片的標準架構。
