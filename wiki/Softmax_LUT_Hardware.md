# Softmax LUT Hardware Acceleration

在探討論文中的長文本注意力機制瓶頸時，指數函數運算是極大的硬體負擔。

## 架構提案：PWL LUT Softmax Engine
我們設計了基於查表 (Look-Up Table) 與分段線性近似 (Piecewise Linear) 的硬體單元：
1. **SRAM LUT：** 將指數曲線離散化儲存。
2. **Shift-Add ALU：** 取代昂貴的 FPU。

## 實測數據
根據 `softmax_lut_sim.py` 的模擬，此硬體協同設計能將 Softmax 延遲從 40.12 ms 壓縮至 15.78 ms，達成 **2.54x** 的加速。