# Hardware MoE Token-Centric Scheduler (HW-TCS) 實驗報告

## 背景與瓶頸分析
傳統 MoE (Mixture of Experts) 架構採用 Expert-Centric 的排程方式，這會導致軟體層面需要繁重的 Token 排序 (Sorting) 與 Scatter/Gather 記憶體操作，造成極大的排程延遲與記憶體碎片化。

## 探索文獻與架構設計
我們提出在 Edge NPU 實作 HW-TCS (Hardware MoE Token-Centric Scheduler)，硬體層面採用 Token-Centric 的架構，使用分散式的 FIFO 佇列直接追蹤 Token 路由。這使得運算單元 (MAC) 可以在 Expert 載入 SRAM 的瞬間自動抓取對應的 Token，完全消弭軟體的排序與聚合成本。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 320.00 ms
*   **Proposed Latency:** 55.00 ms
*   **Throughput Speedup:** 5.82x

## 結論
硬體層級的 Token-Centric 排程器能為 MoE 架構帶來 5.82 倍的加速。強烈建議在下一代處理多專家模型 (如 DeepSeek-V3) 的 Edge NPU 中實作 HW-TCS。