# 硬體稀疏門控引擎 (HW-SGE) 模擬報告

## 1. 摘要
在處理 64K 以上長文本時，Attention 機制中大量 Token 之間的關聯度極低（接近於零）。軟體通常需要計算完整的 Dense 矩陣後再進行 Masking，造成鉅額算力浪費。本研究提出並驗證「硬體稀疏門控引擎 (Hardware Sparse Gating Engine, HW-SGE)」，以動態跳過無效的 MAC 運算。

## 2. 實驗結果
* 測試規模: 64K Context, 32 Heads, 128 Head Dim
* Baseline 延遲 (軟體 Dense 計算): 175946.86 ms
* HW-SGE 延遲: 26396.28 ms
* 吞吐量加速比: 6.67x
* 節省的 MAC 運算量: 85.0%

## 3. 硬體架構建議
建議在 Edge NPU 的 Tensor Core 陣列前緣加入「HW-SGE 預測器」，利用超低精度 (如 INT2 或 INT4) 快速評估 QK 點積的重要性，並對低分區塊直接進行 Clock Gating (時脈閘控)，這不僅能達成 6.67 倍的加速，還能省下極為可觀的動態功耗。