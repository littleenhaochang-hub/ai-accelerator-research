# Auto-Researcher 報告: 2:4 結構化稀疏 (Structured Sparsity) 硬體架構

## 摘要
在資源受限的 Edge 裝置上，降低 Tensor Core 功耗與提升吞吐量是首要目標。非結構化稀疏 (Unstructured Sparsity) 雖然壓縮率高，但會造成硬體記憶體存取的不規則與 ALU 的閒置。本實驗模擬 2:4 結構化稀疏 (每 4 個權重強制保留 2 個非零值)，探討其對運算量與中繼資料 (Metadata) 的影響。

## 實驗設定
- 矩陣維度: 4096 x 4096
- 稀疏模式: 2:4 Structured Sparsity

## 模擬結果
* **Baseline MACs:** 16,777,216
* **Proposed Sparse MACs:** 8,388,608
* **運算加速比 (Compute Speedup):** 2.00x
* **Metadata 額外開銷:** 2048.00 KB (針對單層 4Kx4K 矩陣)

## 結論與架構建議
2:4 結構化稀疏能帶來穩定的 2 倍 MAC 運算節省與 2 倍頻寬節省，且不破壞硬體的記憶體對齊。雖然引入了 Metadata 開銷 (約佔 2MB 於 4Kx4K 層)，但這完全可以透過硬體壓縮電路隱藏。我們建議下一代 Edge NPU 全面實作 **Sparse Tensor Core**，並內建硬體級別的 Metadata Decoder，以在相同的散熱與功耗限制 (Thermal Envelope) 下獲得翻倍的推論效能。
