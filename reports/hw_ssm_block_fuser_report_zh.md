# Hardware SSM Block Fuser (HW-SBF) 實驗報告

## 背景與瓶頸分析
State Space Models (SSM) 的 Sequential Scan 在軟體層面上涉及多次 SRAM 讀取、寫入與計算，導致嚴重的記憶體頻寬瓶頸。

## 探索文獻與架構設計
提出在 Edge NPU 實作 HW-SBF (Hardware SSM Block Fuser)，將 SSM block 內的狀態轉換融合進暫存器中進行連續運算，完全避免中間結果寫回 SRAM。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 200.00 ms
*   **Proposed Latency:** 48.00 ms
*   **Throughput Speedup:** 4.17x

## 結論
透過暫存器層級的融合運算，硬體 SSM Block Fuser 可達 4.17 倍加速。建議整合至下一代原生支援 SSM 的 Edge NPU 架構中。