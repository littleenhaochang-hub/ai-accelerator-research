# LUT-based MAC for Sub-4-bit Quantization
## 背景 (Background)
在極低位元量化 (W4A4 或更低) 的情況下，運算元的值域非常小 (例如 4-bit 只有 16 種可能值)。與其使用傳統的乘法器 (Multiplier)，不如將所有可能的乘積預先計算好存入 Look-Up Table (LUT) 中。

## 模擬參數 (Parameters)
- Hidden Dimension: 4096
- INT4 MAC 能量: 0.1 pJ
- LUT 讀取能量: 0.02 pJ
- 累加器能量: 0.01 pJ

## 模擬結果 (Results)
- INT4 運算總能耗: 1.68 µJ
- LUT 查表與累加總能耗: 0.50 µJ
- 能效提升比: 3.33x

## 架構建議 (Architectural Proposal)
為了極致降低 Edge NPU 的功耗，我們建議在 Tensor Core 內部整合分散式的 **Micro-SRAM LUTs**。當載入 W4A4 甚至 W2A2 的權重時，MAC Array 動態重構為 LUT 查表模式，完全關閉耗電的組合邏輯乘法器，僅保留加法樹，達成約 3.33 倍的推論能效提升。
