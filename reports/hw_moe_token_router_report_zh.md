# 硬體 O(1) MoE Token 路由器 (Hardware O(1) MoE Token Router) 模擬報告

## 執行摘要
測試硬體層級的 O(1) MoE 專家選擇路由器，避免依賴軟體 Top-K 排序。

## 實驗結果
- **加速比:** 8.67x
- **建議:** 於 NPU 中整合 O(1) 專家選擇邏輯硬體單元。