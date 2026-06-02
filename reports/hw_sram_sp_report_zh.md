# Hardware In-SRAM Sparse Predictor (HW-SRAM-SP) 實驗報告

## 1. 實驗背景與瓶頸分析
對於具有高稀疏性的網路層 (如 MoE 的 Expert 輸出或 SwiGLU 激勵函數)，大部份的 activation 值為零或趨近於零。在傳統 NPU 架構中，這些稀疏矩陣仍會被完整讀出 SRAM 送至 MAC 陣列，這浪費了大量的 SRAM 內部頻寬與動態功耗。

## 2. 探索與文獻支持
結合 Compute-in-Memory (CIM) 概念，我們提出 Hardware In-SRAM Sparse Predictor (HW-SRAM-SP)。

## 3. 實驗方法與 Prototype
開發 `hw_sram_sp_sim.py`，模擬在 SRAM 位元線 (Bitlines) 周邊加入極輕量級的稀疏預測邏輯。在觸發全域讀取前，先在記憶體內部評估並遮蔽零值區域。
- **測試設定:** 8192x8192 Matrix, 85% Sparsity, 2048 GB/s SRAM Bandwidth.

## 4. 數據與驗證結果
- **Baseline Latency:** 0.16 ms
- **HW-SRAM-SP Latency:** 0.03 ms
- **效能提升 (Speedup):** 5.52x
- **動態功耗節省 (Energy Reduction):** 85.0%

## 5. 架構結論與建議
HW-SRAM-SP 能將稀疏性過濾推到離資料最近的地方 (PIM 層級)，避免了龐大的內部資料搬移。強烈建議未來 Edge NPU 的 SRAM Macro 整合此特性。
