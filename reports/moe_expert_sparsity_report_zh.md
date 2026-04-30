# Hardware MoE Expert Sparsity Predictor 實驗報告

## 1. 實驗背景
對於擁有極大專家數量的 MoE 模型（如 8192 專家），找出 Top-K 並過濾掉極低機率的專家在軟體上需要大量的排序與分支運算，導致推論延遲。

## 2. 實驗方法
設計 `moe_expert_sparsity_sim.py`，模擬一個硬體級的 MoE 專家稀疏預測器 (Hardware MoE Expert Sparsity Predictor)，直接在 NPU 的路由單元中加入平行的 Logit 比較器，以硬體過濾掉無效的專家喚醒。

## 3. 實驗數據與結果
*   **專家數量:** 8192
*   **軟體剪枝延遲:** 40.96 ms
*   **硬體剪枝延遲:** 0.82 ms
*   **吞吐量加速比:** 50.00x

## 4. 架構建議
硬體層級的平行比較器能大幅減少 Top-K 排序與過濾的開銷。建議將此「Hardware MoE Expert Sparsity Predictor」與先前的硬體 Top-K 網路結合，設計在下一代 Edge NPU 中，以處理未來破萬專家的超大規模 MoE 模型。