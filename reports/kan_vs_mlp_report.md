# KAN (Kolmogorov-Arnold Networks) vs MLP 硬體評估報告

## 執行摘要
KAN (Kolmogorov-Arnold Networks) 是一種新穎的神經網路架構，將傳統 MLP 節點上的非線性激活函數移至邊緣 (Edges) 上，並透過可學習的 Splines (樣條函數) 來取代靜態線性權重。本實驗從 Edge NPU 的 SRAM 容量與算力角度評估 KAN 的硬體可行性。

## 實驗數據與分析
- **MLP 基準**: 單層 FFN 約 1.17e+08 MACs
- **KAN (Grid Size = 5)**: 
  - MAC 運算量: 3.52e+08 (3x 增加，用於 Cubic B-Spline 計算)
  - 記憶體權重數量: 7.05e+08 (6x 增加，每條邊需儲存 G+1 個控制點參數)

## 硬體架構結論
1. **嚴重的記憶體膨脹 (Memory Bloat)**: KAN 雖然在理論上具有更高的參數表達力，但它將每一個權重展開成一組 Spline 係數 (本例為 6 倍)。在記憶體極度受限的 Edge NPU 上，這會導致 SRAM OOM 或極嚴重的 DRAM 頻寬瓶頸 (Memory Wall)。
2. **算力無優勢**: Spline 的求值過程 (B-spline) 會引入額外的乘加運算，導致總 MAC 數量達到傳統 MLP 的 3 倍。
3. **結論**: 在沒有特殊「Spline-Compression Hardware (樣條函數硬體壓縮引擎)」的情況下，純軟體或一般 Tensor Core 執行 KAN 會遭遇極大的效能倒退。短期內不建議將其納入 Edge LLM 架構。
