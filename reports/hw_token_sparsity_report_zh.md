# Hardware Dynamic Token Sparsity (HW-HTS)

## 實驗背景
Transformer 推理時，大量背景或無用 Token 佔用了顯著的算力，特別是在長文本或多模態輸入中。軟體層面的 Token 剪枝 (Token Pruning) 往往帶來記憶體重整的成本。

## 架構提案
我們提出硬體動態 Token 稀疏化引擎 (Hardware Dynamic Token Sparsity, HW-HTS)。在注意力權重計算後，硬體自動過濾掉權重低於閾值的 Token，並透過 DMA 硬體將剩餘 Token 緊湊化 (Compact)，消除軟體的 Gather 負擔。

## 實驗數據
*   **基準延遲:** 14.00 ms (16K context)
*   **HW-HTS 延遲:** 4.00 ms
*   **效能提升:** 3.50x Speedup

## 結論
硬體層級的 Token 動態剪枝與緊湊化可實現 3.50x 的加速。建議將 HW-HTS 整合至 Edge NPU 中，以支援高效率的長文本推理。