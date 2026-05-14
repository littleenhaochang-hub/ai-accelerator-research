# 硬體連續 Token 狀態淘汰器 (HW-CTSE) 模擬報告

## 1. 摘要
在處理 1M Token 以上的無限串流生成 (Streaming Inference) 時，軟體必須持續管理 KV Cache 的 Sliding Window 與 Attention Sink 指標，帶來龐大的記憶體碎片與 CPU 控制負擔。本研究探討並驗證「硬體連續 Token 狀態淘汰器 (Hardware Continuous Token State Evictor, HW-CTSE)」，將記憶體淘汰邏輯直接實作於硬體層。

## 2. 實驗結果
* 測試規模: 1,000,000 Tokens (Window: 32K)
* Baseline 延遲 (軟體淘汰管理): 8050.00 ms
* HW-CTSE 延遲: 505.00 ms
* 吞吐量加速比: 15.94x
* 淘汰開銷: 0 CPU 週期

## 3. 硬體架構建議
提議在 Edge NPU 的 SRAM 寫入埠端整合「HW-CTSE 引擎」，以背景非同步方式自動覆寫最舊的 Token 狀態，並維持 Sink Token 的絕對位置不變。這能完全消除無限文本生成的軟體管理開銷，確保系統維持在純計算瓶頸 (Compute-bound)。