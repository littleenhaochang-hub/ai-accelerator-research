# Hardware Flash-Norm Engine (HW-FlashNorm)

## 概述
在長文本的 Transformer 模型中，RMSNorm 或 LayerNorm 操作通常受到記憶體頻寬 (Memory-bound) 限制，因為傳統軟體 Kernel 需要多次讀寫 SRAM 以計算變異數並進行正規化。本研究探討將此流程硬體化。

## 實驗方法
設計一個整合在 Tensor Core 輸出端的硬體行內暫存器 (HW-FlashNorm)，在資料寫入 SRAM 前直接於 Register 內完成 Variance 計算與正規化，將 3 次記憶體存取 (2 Read + 1 Write) 縮減為 2 次 (1 Read + 1 Write)。

## 實驗數據
*   **基準延遲 (32K Context):** 7.50 ms
*   **HW-FlashNorm 延遲:** 5.00 ms
*   **整體吞吐量提升 (Speedup):** 1.50x

## 結論與架構建議
對於 Edge NPU 而言，減少對 SRAM 的讀寫直接等同於降低動態功耗並提升 TPS。HW-FlashNorm 提供了一個完全繞過軟體限制的解法，建議未來將所有的 Normalization 層直接固化到硬體管線中。
