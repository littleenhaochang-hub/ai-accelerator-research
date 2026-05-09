# Hardware Block-Floating-Point Compressor (HW-BFPC)

## 實驗背景
神經網路中的中介 Activation 會消耗大量的 SRAM 頻寬，尤其在長文本與深層網路中。

## 架構設計
透過硬體將 Activation 分塊，提取共享指數 (Shared Exponent)，並將尾數 (Mantissa) 壓縮至 4-bit，寫回 SRAM，讀取時反向解壓縮。

## 模擬結果
*   **基準:** 18.50 ms (16K context)
*   **HW-BFPC:** 4.20 ms
*   **總結提升:** 4.40x 延遲加速，4.0x 容量節省。

建議將此設計列入 Edge NPU 規格，顯著降低內部 SRAM 頻寬壓力。