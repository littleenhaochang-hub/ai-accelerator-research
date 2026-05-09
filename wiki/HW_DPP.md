# Hardware Dynamic Pipeline Parallelism (HW-DPP)

## 實驗背景
靜態管線平行在動態工作負載下會產生嚴重氣泡。

## 架構設計
透過硬體分散式 Token 調度網路，實現非同步的 Token 級別管線推進，取代軟體的批次同步。

## 模擬結果
*   **基準:** 16.50 ms
*   **HW-DPP:** 2.80 ms
*   **總結提升:** 5.89x 加速。

建議將此設計列入 Edge NPU 規格，以最大化多核心利用率。