# 硬體 Token 裁剪器 (Hardware Token Trimmer) 分析報告

## 執行摘要
在長文本處理 (如 128K context) 中，Prefill 階段的 OOM 是一個重大問題。我們探討了在 SRAM 寫入端直接進行 Token 裁剪的硬體架構。

## 模擬結果
* **軟體裁剪延遲:** 64.00 ms
* **硬體 Inline 裁剪延遲:** 1.28 ms
* **效能提升:** 延遲加速達 50.00x。
* **記憶體節省:** 記憶體容量需求降低 5.00x。

## 架構建議
針對未來的邊緣 NPU 架構，強烈建議整合 **Hardware Token Trimmer**，利用注意力分數動態裁剪無用 Token，避免進入 DRAM。
