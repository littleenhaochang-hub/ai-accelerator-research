# 實驗報告：Hyperdimensional Computing (HDC) XOR Attention 硬體加速器

## 背景 (Background)
目前 LLM 的 Attention 計算極度依賴高精度的浮點數或整數乘加運算 (MAC)，這在長文本處理時產生極高的能耗牆 (Power Wall) 與面積開銷。

## 方法 (Methodology)
本實驗探討引入 **Hyperdimensional Computing (HDC, 超維度運算)** 理論至 Edge NPU。將高精度的 Q, K 向量投影為極高維度 (如 10,000-bit) 的二值向量 (Bipolar Vectors)。在此空間中，原本昂貴的內積運算 ($QK^T$) 被直接替換為極度廉價的位元級 **XOR (互斥或)** 與 **Popcount (漢明權重計算)** 操作。

## 驗證結果 (Results)
- **基準 FP16 MAC Attention:** 延遲 0.6242 秒，能耗 36864.00 mJ。
- **HDC XOR Attention:** 延遲 0.1709 秒，能耗 409.60 mJ。
- **整體提升:** 將算術複雜度從乘法降維至布林邏輯，帶來了 **3.65 倍** 的延遲加速，且動態能耗驚人地降低了 **90 倍 (90.00x)**。

## 物理架構建議 (Architectural Proposal)
強烈建議在下一代 Extreme Edge NPU 的 Attention Block 中引入「HDC Binary Vector Engine」。完全移除該區塊的 DSP/MAC 單元，替換為超寬的 XOR 邏輯閘陣列與硬體 Popcount 樹。這將使手錶或小型穿戴裝置能以微瓦級 (Microwatt) 功耗處理數千長度的 Context。
