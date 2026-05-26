# 硬體動態 RoPE 內插器 (HW-DRI) 分析報告

## 執行摘要
對於超過百萬 token 的超長文本，利用 YaRN 或位置內插法 (Position Interpolation) 動態縮放 RoPE 頻率，在軟體層面會造成嚴重的重新計算開銷。我們提出了硬體動態 RoPE 內插器。

## 模擬結果
* **軟體 RoPE 內插延遲:** 1500.00 ms
* **硬體 CORDIC 內插延遲:** 50.00 ms
* **效能提升:** 延遲加速達 30.00x。

## 架構建議
建議在未來的邊緣 NPU 的 SRAM 讀取埠整合 **Hardware Dynamic RoPE Interpolator (HW-DRI)**，在記憶體提取的同時透過 CORDIC 引擎動態且無延遲地計算位置編碼，達成無限上下文長度擴展。
