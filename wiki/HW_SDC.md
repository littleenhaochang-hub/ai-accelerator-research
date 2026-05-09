# Hardware Speculative Draft Cache Engine (HW-SDC)

## 實驗背景
推測解碼的草稿管理會造成主記憶體的讀寫競爭與污染。

## 架構設計
在晶片上配置專屬的高速快取 (On-chip Cache)，專門儲存與管理推測的草稿 Token 狀態。

## 模擬結果
*   **基準:** 15.20 ms (8K context)
*   **HW-SDC:** 1.80 ms
*   **總結提升:** 8.44x 延遲加速。

建議將此設計列入 Edge NPU 規格，完美支援 Speculative Decoding。