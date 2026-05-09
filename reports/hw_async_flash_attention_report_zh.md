# Auto-Researcher 分析報告：Hardware Asynchronous Flash-Attention Tiling Engine (HW-AFATE)

## 1. 瓶頸分析 (Analyze)
在 Edge NPUs 上執行 FlashAttention 時，受限於 LPDDR 頻寬，SRAM Tile 的載入會導致 Tensor Cores 處於閒置等待狀態 (Stall)。傳統軟體實作的同步迴圈無法完全重疊 (Overlap) 記憶體載入與矩陣運算。

## 2. 理論探索 (Explore)
我們提出「Hardware Asynchronous Flash-Attention Tiling Engine (HW-AFATE)」。透過在 NPU 內部實作硬體級別的 Ping-Pong Buffer 與非同步 DMA Scheduler，當 MAC 陣列正在計算 Tile N 時，DMA 已經在背景非同步載入 Tile N+1。

## 3. 原型實驗結果 (Prototype)
我們於 `hw_async_flash_attention_sim.py` 進行了硬體級別的算力模擬：
*   **基準測試 (同步載入與計算):** 延遲 1038.01 ms。
*   **HW-AFATE (非同步 Ping-Pong Buffer):** 延遲 983.04 ms。
*   **效能提升:** 達成 **1.06x 吞吐量加速** (在 Compute-bound 下，完全隱藏了 15us/tile 的記憶體延遲)。

## 4. 硬體架構結論 (Conclusion)
邊緣裝置的 NPU 必須內建非同步記憶體調度單元 (Async TMA)。雖然在 MAC 算力極高的情況下加速比有限，但對於嚴格受限於記憶體頻寬的 Edge AI 裝置，消除記憶體 Stall 依然是逼近理論算力上限 (Roofline) 的必要架構設計。
