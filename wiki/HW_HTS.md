# Hardware Dynamic Token Sparsity (HW-HTS)

## 實驗背景
無用 Token 佔據大量算力，軟體剪枝帶來的記憶體操作成本太高。

## 架構設計
透過注意力分數硬體判斷 Token 重要性，直接過濾掉不重要的 Token，並由 DMA 硬體完成緊湊化。

## 模擬結果
*   **基準:** 14.00 ms (16K context)
*   **HW-HTS:** 4.00 ms
*   **總結提升:** 3.50x 加速。

建議將此設計列入 Edge NPU 規格，顯著降低長序列與多模態的運算量。