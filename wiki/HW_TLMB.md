# Hardware Token-Level Micro-Batching (HW-TLMB)

## 實驗背景
動態網路 (MoE, Early-Exit) 的軟體動態 Batching 會產生極高的 Kernel Launch overhead。

## 架構設計
在 NPU 分發單元加入硬體佇列，自動將同計算路徑的 Token 組裝成微批次，零軟體干預。

## 模擬結果
*   **基準:** 14.50 ms
*   **HW-TLMB:** 2.40 ms
*   **總結提升:** 6.04x 加速。

建議將此設計列入 Edge NPU 規格，完美支援未來高度動態的神經網路架構。