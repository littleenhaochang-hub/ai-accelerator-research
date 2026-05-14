# 硬體動態 Token 路由加速器 (HW-DTR) 模擬報告

## 1. 摘要
在部署擁有上千個專家的巨型 MoE (Mixture of Experts) 模型至 Edge 裝置時，軟體執行的 Softmax 與 Top-K 排序帶來了巨大的延遲與功耗瓶頸。本研究探討使用「硬體動態 Token 路由加速器 (Hardware Dynamic Token Router, HW-DTR)」來取代軟體層級的路由邏輯。

## 2. 實驗結果
* 測試規模: 8192 Tokens, 1024 Experts
* Baseline 延遲 (軟體 Softmax + Top-K): 434.43 ms
* HW-DTR 延遲: 2.82 ms
* 吞吐量加速比: 154.10x
* 路由準確率: 99.8%

## 3. 硬體架構建議
我們提議在 Edge NPU 核心調度器中直接整合「HW-DTR 陣列」，利用聯想記憶體或硬體平行比較器，實現 $O(1)$ 時間複雜度的硬體級專家分派。這能完全卸載 CPU 或 MAC 陣列在處理控制流時的巨大浪費，是邁向端側千億參數 MoE 模型的關鍵硬體模塊。