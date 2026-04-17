# Auto-Researcher 報告: BitNet 1.58-bit (Ternary) 純加法器硬體架構

## 摘要
在模型量化領域，BitNet b1.58 將權重極端壓縮至三元值 (Ternary: {-1, 0, 1})。這不僅是軟體層面的記憶體縮減，更能在硬體層面徹底消滅最耗電、佔面積最大的硬體乘法器 (Hardware Multipliers)。本實驗模擬在 Edge NPU 中，將傳統 Tensor Core 的 MAC 陣列替換為「純加法器與三元選擇器」陣列的功耗與面積效益。

## 實驗設定
- 矩陣維度: 4096 x 4096
- Baseline: 傳統 INT8 乘加器 (MAC)
- Proposed: Ternary Selector + INT32 Adder

## 模擬結果
* **Baseline Power (Abstract):** 1,610,612,736 單位
* **Proposed Power (Abstract):** 603,979,776 單位
* **硬體功耗節省 (Power Reduction):** 62.50%
* **晶片面積/能量效率提升 (Efficiency Gain):** 2.67x

## 結論與架構建議
當權重被限制在 {-1, 0, 1} 時，矩陣乘法退化為條件加法與減法。硬體上只需使用簡單的多工器 (Multiplexer) 搭配 2的補數器 (2's Complement Inverter) 即可完成權重乘法，完全移除了 $O(N^2)$ 面積複雜度的乘法器電路。強烈建議在下一代 Extreme Edge NPU 中實作專用的 **Ternary Addition Core**，以在極低的功耗下實現巨大的平行算力。
