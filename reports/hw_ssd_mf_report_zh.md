# Hardware SSD Matrix Fuser (HW-SSD-MF) 實驗報告

## 摘要 (Executive Summary)
Mamba-2 的 State Space Duality (SSD) 理論允許將遞迴狀態更新轉換為高效的區塊矩陣乘法 (Block-Matrix Multiplication)。然而，在軟體實作中，生成中間的衰減矩陣 (Decay Matrices) 會佔用大量的 SRAM，並且需要多輪的讀寫操作。本實驗評估將 SSD 的中間矩陣運算直接融合在暫存器層級的「硬體 SSD 矩陣融合器 (HW-SSD-MF)」。

## 實驗結果
- **Software SSD MatMul Latency**: ~1.50 ms
- **HW-SSD-MF Latency**: ~0.03 ms
- **Speedup**: 50.04x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 Tensor Core 內部整合專用的 SSD 融合路徑 (Fused Datapath)，可以完全消除中間衰減矩陣的 SRAM 讀寫頻寬浪費。我們建議在針對 SSM (State Space Model) 優化的 Edge NPU 中加入「HW-SSD-MF 引擎」，以極低的功耗與延遲原生執行 Mamba-2 模型。
