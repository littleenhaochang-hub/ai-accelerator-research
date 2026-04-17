# LUT-based Sub-4-bit Hardware Architecture

## 實驗背景
對於極低精度的推論 (Sub-4-bit)，乘法器 (Multiplier) 的面積與功耗效益驟降。如果將運算元視為索引，可以直接利用 SRAM 查表 (Look-Up Table) 來取代乘法。

## 硬體模擬與分析
- **腳本**: `lut_mac_sim.py`
- INT4 MAC 預估耗能 0.1 pJ，而 SRAM 查表加累加耗能 0.03 pJ。
- **能效比**: 查表法比傳統整數乘法提升了 **3.33x** 的能效。

## 架構協同設計結論
Edge AI 晶片應設計可重構的 Tensor Core：當執行 INT8 時使用傳統 MAC，而當執行 W4A4/W2A2 時，將乘法器關閉，動態將鄰近的暫存器配置為 **Micro-SRAM LUTs**，將計算徹底轉化為 Memory Read 與 Addition，大幅降低 mW 等級的功耗。
