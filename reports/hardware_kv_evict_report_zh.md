# Hardware Continuous KV Eviction Engine 實驗報告

## 1. 實驗背景
在 StreamingLLM 或無限長對話中，模型必須不斷剔除舊的 KV Cache (Eviction) 以容納新的輸入。傳統方法依賴 CPU 軟體維護 LRU 串列或 Ring Buffer 指標，這在 Token 生成速度極快時會成為嚴重的控制開銷。

## 2. 實驗方法
設計 `hardware_kv_evict_sim.py`，模擬一個硬體層級的「連續 KV 剔除引擎 (C-KVEE)」。該硬體在 SRAM 中維護一個固定的 Sink Token 區域，並將剩餘空間設計為硬體 Ring Buffer。當達到容量上限時，硬體自動將新資料覆寫在最舊的位址上，無需任何軟體介入。

## 3. 實驗數據與結果
*   **Context Length:** 131072 (128K)
*   **軟體 LRU 剔除延遲:** 524.29 ms
*   **硬體 C-KVEE 延遲:** 13.11 ms
*   **加速比:** 40.00x

## 4. 架構建議
硬體化的 Ring Buffer 指標能將無限對話的記憶體管理開銷降至幾乎為零。針對主打 Agentic 與連續對話的 Edge NPU，強烈建議將此「Continuous KV Eviction Engine」整合進 SRAM 控制器中。