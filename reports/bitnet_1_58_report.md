# BitNet 1.58-bit (Ternary) Hardware Energy Report
## 背景 (Background)
BitNet b1.58 將 LLM 的權重量化為 {-1, 0, 1}，徹底淘汰了高能耗的浮點/整數乘法器，將矩陣乘法轉換為純加減法運算。

## 模擬參數 (Parameters)
- Hidden Dimension: 4096
- INT8 MAC Energy: 0.2 pJ
- INT Add Energy: 0.05 pJ
- Ternary Sparsity (Zeros): 20%

## 模擬結果 (Results)
- 傳統 INT8 運算能耗: 3355.44 nJ
- BitNet 純加法運算能耗: 671.09 nJ
- 硬體能效提升比 (Energy Efficiency Gain): 5.00x

## 架構建議 (Architectural Proposal)
未來的 Edge NPU 應配置專屬的 **Ternary ALU Arrays (三元加法器陣列)**，完全移除這些 Core 的 Multiplier 單元以節省矽面積 (Area)。配合權重中 0 的稀疏性 (Sparsity)，硬體應具備 Zero-Skipping 機制，達成 5.00 倍以上的推論能效提升，這對於依靠電池供電的終端裝置至關重要。
