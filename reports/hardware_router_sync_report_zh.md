# Hardware MoE Async Router Crossbar 實驗報告

## 1. 實驗背景
在具有上千個專家的 MoE 模型 (如 DeepSeek 系列) 中，路由選擇的結果通常需要從 GPU/NPU 同步回 CPU，以便 CPU 知道接下來要 Launch 哪些專家的 Kernel 或是從 RAM 搬運哪些權重。這個硬體與軟體之間的同步屏障 (Synchronization Barrier) 是效能殺手。

## 2. 實驗方法
設計 `hardware_router_sync_sim.py`，模擬將 MoE 的路由分配與 Kernel/DMA 排程完全下放到硬體的「非同步路由交換機 (Async Router Crossbar)」。硬體算出 Top-K 專家後，直接觸發內部的 DMA 控制器，無需等待 CPU 介入。

## 3. 實驗數據與結果
*   **專家數量:** 2048
*   **軟體同步延遲:** 16.38 ms
*   **硬體非同步交換機延遲:** 0.31 ms
*   **加速比:** 53.33x

## 4. 架構建議
極端的 MoE 效能優化必須打破 CPU 與 NPU 之間的依賴。建議未來的 Edge NPU 將「Hardware MoE Async Router Crossbar」與 DMA 控制器直接綁定，達成完全自主的硬體層級權重抓取與運算排程。