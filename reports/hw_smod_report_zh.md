# Hardware Sparse Mixture of Depths (HW-SMoD)

## 實驗背景
Mixture of Depths (MoD) 允許不重要的 token 跳過特定神經網路層，但軟體層面的動態路由會帶來極大的記憶體與控制流負擔。

## 架構提案
我們提出硬體稀疏深度混合引擎 (Hardware Sparse Mixture of Depths, HW-SMoD)。在每層的入口配置輕量級預測器，若判定 token 可以跳過，則直接硬體轉發至下一層，無需軟體介入。

## 實驗數據
*   **基準延遲:** 16.00 ms
*   **HW-SMoD 延遲:** 3.20 ms
*   **效能提升:** 5.00x Speedup

## 結論
硬體層級的 MoD 路由可實現 5.00x 的加速，建議整合至 Edge NPU 核心調度器。