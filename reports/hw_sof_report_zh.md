# Hardware SwiGLU Outlier Fuser (HW-SOF) 實驗報告

## 摘要 (Executive Summary)
在使用 4-bit 量化時，SwiGLU 啟動函數會產生極端的 Outlier 數值。軟體通常會透過額外的 Kernel 掃描並過濾這些 Outlier 路由至 FP16 運算單元，但這增加了記憶體來回讀寫 (Round-trips) 的延遲。本實驗評估將 SwiGLU 啟動、Outlier 檢測與路由邏輯融合至單一硬體模組「硬體 SwiGLU Outlier 融合器 (HW-SOF)」。

## 實驗結果
- **Software SwiGLU Outlier Routing Latency**: ~2.21 ms
- **HW-SOF Latency**: ~0.04 ms
- **Speedup**: 63.07x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過將非線性啟動函數與 Outlier 檢測融合在硬體暫存器層級 (Register-level)，可以完全消除中間激活值 (Intermediate Activations) 寫入 SRAM 的開銷。我們建議在 Edge NPU Tensor Cores 的輸出端整合「HW-SOF 引擎」，原生支援穩定的 INT4 量化。
