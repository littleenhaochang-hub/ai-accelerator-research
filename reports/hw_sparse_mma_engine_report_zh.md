# 硬體稀疏矩陣乘加引擎 (Hardware Sparse MMA Engine) 模擬報告

## 執行摘要
測試專為 2:4 與 4:8 結構化稀疏設計的硬體 Sparse MMA 引擎，消除軟體 Scatter/Gather 所造成的記憶體頻寬瓶頸。

## 實驗結果
- **軟體稀疏收集延遲:** 76.50 ms
- **硬體稀疏 MMA 延遲:** 8.80 ms
- **加速比:** 8.69x
- **建議:** 於 NPU 核心整合原生的 Sparse MMA 硬體邏輯，提升推論吞吐量。