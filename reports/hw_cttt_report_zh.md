# Hardware Continuous Test-Time Training (HW-CTTT)

## 實驗背景 (Background)
邊緣裝置 (Edge NPU) 若要進行持續學習或 Test-Time Training (TTT)，傳統的 Backpropagation (反向傳播) 需要儲存龐大的 Activation Checkpoints，這會瞬間耗盡 SRAM 甚至 LPDDR 的頻寬與容量。

## 實驗設計 (Methodology)
本實驗設計了硬體級 Forward-Gradient (前向梯度) 學習引擎 (`hw_cttt_sim.py`)。透過硬體層面的 Forward-Gradient 演算法，在模型進行 Forward Pass 的同時，直接於 SRAM 中以極低精度更新權重，完全免除 Backward Pass 與 Activation 儲存的記憶體開銷。

## 實驗結果 (Results)
- Software Backprop Latency: 0.0550 s
- HW-CTTT Latency: 0.0018 s
- **Speedup**: 29.82x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 內建「HW-CTTT 引擎」。此架構將使 Edge 裝置能以極低功耗進行真正的即時、無記憶體瓶頸的持續學習 (Continuous Learning)，完全符合 Test-Time Compute 的發展趨勢。