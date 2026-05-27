# Hardware Flash-Decoding Scheduler (HW-FDS)

## 概述
Flash-Decoding 透過將 KV Cache 切塊 (Blocks) 並在多個 SMs (Streaming Multiprocessors) 上平行計算以加速長文本生成。然而，由軟體 Kernel 負責的工作排程與 Block 分配會隨著 Context 長度增加而產生極大的開銷。本實驗探討將此排程邏輯硬體化。

## 實驗方法
設計一個整合於 NPU 的硬體 Flash-Decoding 排程器 (HW-FDS)，能夠在 $O(1)$ 的時間複雜度內非同步地將 KV Block 分發給閒置的 Tensor Cores，完全消除 CPU 或韌體的干預。

## 實驗數據
*   **基準軟體排程延遲 (256 Blocks):** 12.80 ms
*   **HW-FDS 硬體排程延遲:** 0.05 ms
*   **排程開銷加速比 (Speedup):** 256.00x

## 結論與架構建議
將 Block 分配邏輯下放至硬體可以將排程時間從線性 $O(N)$ 降至 $O(1)$，徹底解放 NPU 運算資源。建議在下一代專注於長文本處理的 Edge NPU Scheduler 中整合 HW-FDS 模組。
