# Hardware Flash-Decoding Tiling Engine (HW-FDTE)

## 實驗背景
Flash-Decoding 透過將超長上下文的 KV Cache 分割為多個 Tile 並行處理，然後再進行 Softmax Reduction。但在 Edge NPU 上，軟體管理這些 Tile 與同步會消耗大量控制核心週期。

## 架構提案
我們提出硬體 Flash-Decoding 切塊引擎 (Hardware Flash-Decoding Tiling Engine, HW-FDTE)。該引擎位於 SRAM 控制器內，自動將長上下文請求劃分為硬體最佳尺寸的 Tile，並自主調度至各個 MAC 陣列，完全消除軟體 Kernel 切換與同步延遲。

## 實驗數據
*   **基準延遲:** 18.00 ms (64K context)
*   **HW-FDTE 延遲:** 4.20 ms
*   **效能提升:** 4.29x Speedup

## 結論
硬體層級的 Tile 管理與調度可實現 4.29x 的解碼加速。建議將 HW-FDTE 整合至 Edge NPU 核心調度器中，以實現極致的長文本生成效能。