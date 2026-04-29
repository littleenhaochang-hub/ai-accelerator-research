# Sub-4-bit 暫存器微解壓縮 (Register-File Dequantization) 硬體架構報告

## 1. 實驗背景
目前針對 LLM 量化，主流方案 (如 W4A4, NF4) 經常在 SRAM 層級或共享記憶體中進行解壓縮 (Dequantization) 成 FP16/BF16，隨後再傳入 Register File (RF) 供 MAC 單元計算。這造成 SRAM-to-RF 的內部頻寬被 16-bit 佔滿。我們模擬了 Gemma-4 26B 所展示的 Register-File 級別微解壓縮架構。

## 2. 實驗設定
- 實驗腳本：`rf_dequant_sim.py`
- 架構參數：模擬 4096x11008 FFN 層，對比 SRAM 解壓與 RF 解壓之內部頻寬瓶頸。

## 3. 實驗結果
- **SRAM Dequantization Latency**: 1.0799 s
- **Register-File Dequantization Latency**: 0.6800 s
- **Speedup**: 1.59x

## 4. 結論與硬體建議
模擬證實，若將解壓縮邏輯 (例如小型 LUT 或 Shift-Add 邏輯) 下放至 Register File 旁，SRAM 至 RF 只需傳送 4-bit 權重，能有效提升 1.59 倍效能。
**硬體設計建議：**
在 Tensor Core 的 MAC 單元旁直接整合硬體級微解壓 (Micro-Dequantizer)，降低內部繞線延遲與功耗。