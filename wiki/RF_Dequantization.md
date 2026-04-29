# Register-File Dequantization (RF微解壓縮)

## 瓶頸
傳統 W4A4 或 NF4 量化在 SRAM 層級還原為 FP16，使得 SRAM-to-MAC (Register File) 的頻寬佔用大增，功耗居高不下。

## 解決方案
在 Tensor Core MAC 陣列的 Register File 旁邊直接佈建極低功耗的 Micro-Dequantizer (利用 LUT 或移位加法器)，SRAM 只傳輸 4-bit 權重。

## 數據
- SRAM Dequantization: 1.0799 s
- RF Dequantization: 0.6800 s
- 提升倍率: 1.59x