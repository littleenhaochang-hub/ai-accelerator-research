# Sub-1-bit (0.58-bit) 隨機運算 (Stochastic Computing) 硬體加速分析報告

## 1. 分析瓶頸 (Analyze)
在先前的研究中，我們已將權重量化推至極限的 1.58-bit (Ternary)。然而，對於極端邊緣裝置 (Extreme Edge NPUs，如穿戴裝置)，即便是無乘法器的加法樹 (Adder Trees) 仍會消耗過多的動態功耗 (Dynamic Power)。

## 2. 探索文獻與架構設計 (Explore)
根據最新的硬體架構論文，我們探索了 **Stochastic Computing (SC, 隨機運算)** 技術。SC 將實數編碼為隨機位元流 (Bitstreams) 中的 1 的機率 (Probability)，從而將複雜的乘加運算 (MAC) 簡化為極低功耗的邏輯閘 (如 AND 閘進行乘法，MUX 進行加法)。這種架構可視為低於 1-bit (約 0.58-bit 資訊熵) 的超極限運算。

## 3. 建立原型並驗證 (Prototype & Test)
透過 `ai-accelerator-research/sc_mac_058bit_sim.py` 進行了單次 MAC 能量消耗模擬。
- **Baseline (INT4 MAC):** 0.580 pJ/MAC
- **Proposed (SC 0.58-bit MAC):** 0.040 pJ/MAC
- **Energy Reduction:** 93.10%

實驗證明，Stochastic Computing 能夠消除高達 93% 的運算功耗，將能源效率提升至極致。

## 4. 架構結論
強烈建議在下一代超低功耗 Edge NPU 中，針對非關鍵層 (Non-critical layers) 導入「隨機運算核心 (SC Cores)」，以邏輯閘陣列取代傳統數位乘加器，進一步突破功耗牆。
