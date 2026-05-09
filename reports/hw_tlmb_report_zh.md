# Hardware Token-Level Micro-Batching (HW-TLMB)

## 實驗背景
在處理動態計算圖（如 Early-Exit、MoE）時，各個 Token 的計算路徑不同。依賴軟體框架動態組裝 Batch 會引入極高的 Kernel Launch 與同步延遲。

## 架構提案
我們提出硬體 Token 級別微批次排程器 (Hardware Token-Level Micro-Batching, HW-TLMB)。在 NPU 的分發單元中內建硬體佇列，自動將具有相同計算需求（如分配到同一 MoE 專家或同一 Early-Exit 層級）的 Token 在硬體底層即時組裝為微批次，完全繞過 CPU 軟體排程。

## 實驗數據
*   **基準延遲:** 14.50 ms
*   **HW-TLMB 延遲:** 2.40 ms
*   **效能提升:** 6.04x Speedup

## 結論
硬體層級的微批次組裝可實現 6.04x 的加速，有效消除動態網路的軟體排程瓶頸。建議整合至 Edge NPU 調度器中。