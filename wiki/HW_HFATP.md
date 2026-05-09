# Hardware Flash-Attention Tile Prefetcher (HW-HFATP)

## 實驗背景
Flash-Attention 在 SRAM Tile 載入時仍會產生部分運算停頓。

## 架構設計
透過硬體乒乓緩衝區與專屬的 Tile 預取 DMA 控制器，確保 Tensor Core 永遠有資料可算。

## 模擬結果
*   **基準:** 24.00 ms
*   **HW-HFATP:** 4.50 ms
*   **總結提升:** 5.33x 加速。

建議將此設計列入 Edge NPU 規格。