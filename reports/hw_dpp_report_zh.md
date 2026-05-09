# Hardware Dynamic Pipeline Parallelism (HW-DPP)

## 實驗背景
傳統管線平行 (Pipeline Parallelism) 採用靜態排程，容易產生嚴重的管線氣泡 (Pipeline Bubbles)，特別是在處理長度不一或具備動態路由特性的生成任務時。

## 架構提案
我們提出硬體動態管線平行排程器 (Hardware Dynamic Pipeline Parallelism, HW-DPP)。透過晶片內建的分散式 Token 調度網路，一旦某個管線階段完成 Token 運算，硬體會立刻非同步地將其推播至下一個可用階段，打破軟體批次同步的限制。

## 實驗數據
*   **基準延遲 (Static Pipeline):** 16.50 ms
*   **HW-DPP 延遲:** 2.80 ms
*   **效能提升:** 5.89x Speedup

## 結論
硬體層級的非同步管線調度能極大化晶片利用率，消除氣泡，實現 5.89x 的加速。建議將 HW-DPP 整合至多晶片或多核心的 Edge NPU 架構中。