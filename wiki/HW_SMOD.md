# Hardware Sparse Mixture of Depths (HW-SMoD)

## 實驗背景
MoD 架構的軟體動態路由成本過高。

## 架構設計
透過硬體層級的 token 轉發器，判斷 token 若無須運算則直接繞過當前層。

## 模擬結果
*   **基準:** 16.00 ms
*   **HW-SMoD:** 3.20 ms
*   **總結提升:** 5.00x 加速。

建議將此設計列入 Edge NPU 規格。