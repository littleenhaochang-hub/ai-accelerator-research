# Hardware Activation Sparsity Predictor 驗證報告
## 實驗結果
- **密集群體 MAC 能量**: 1.25 pJ
- **稀疏 MAC 能量**: 0.35 pJ
- **能量降低**: 72.00%
- **吞吐量加速**: 2.80x
- **結論**: LLM 中的 FFN 層 (如 SwiGLU) 具有高度的活化稀疏性 (Activation Sparsity)。透過在 MAC 陣列前加入低精度硬體預測器 (Hardware Predictor)，可提早跳過無效的乘加運算，達成 72% 的能耗降低。建議將其納入新一代 Edge NPU 架構中。
