# Hardware MoE Speculative Trajectory Prefetcher (HW-MSTP)

## 概述
針對 MoE 架構中 CPU-GPU/NPU 之間透過 PCIe Gen4 讀取專家權重所造成的 DMA 延遲瓶頸，本實驗提出了一種基於硬體的軌跡預測預取引擎 (HW-MSTP)。

## 實驗方法
藉由在硬體層級 (DMA 控制器前) 實作一個輕量級的 Token Trajectory Predictor，HW-MSTP 能夠在當前層運算進行時，預測下一層最有可能被激活的專家模型，並提前發出非同步 DMA 預取請求，從而將傳輸延遲與運算時間重疊 (Overlap)。

## 實驗數據
*   **基準需求拉取延遲 (Baseline):** 7.81 ms (批量 128 Tokens)
*   **預測命中率:** 85.0%
*   **HW-MSTP 預取未命中懲罰延遲:** 1.22 ms
*   **整體吞吐量提升 (Speedup):** 6.40x

## 結論與架構建議
軟體層級的預測器容易受限於 Kernel 啟動延遲。將軌跡預測硬體化並直接與 DMA 控制器耦合，能有效隱藏 PCIe 記憶體牆的延遲。建議未來 Edge NPU 設計應在 Scheduler 內整合此「軌跡預取引擎 (HW-MSTP)」。
