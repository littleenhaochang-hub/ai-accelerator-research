# Auto-Researcher 分析報告：Hardware MoE Expert Cache Prefetcher (HW-ECP)

## 1. 瓶頸分析 (Analyze)
在 Edge 裝置上執行大型 MoE 模型（如 Mixtral）時，因為 SRAM/VRAM 容量不足，必須頻繁從 NVMe/UFS 載入 Expert 權重。傳統架構下，NPU 計算出 Router 索引後，需要觸發中斷（Interrupt）讓 CPU 介入，由 OS 驅動程式設定 DMA，這會產生約 500us 的嚴重軟體開銷（Software Overhead）。

## 2. 理論探索 (Explore)
我們提出「Hardware MoE Expert Cache Prefetcher (HW-ECP)」。將 DMA 控制器的 Doorbell（門鈴暫存器）直接暴露給 NPU 的 Router 單元。當 NPU 在計算 Layer N 的 Router 時，硬體會自主預測 Layer N+1 的 Expert，並直接對 NVMe 發出 P2P DMA 讀取指令，完全繞過 CPU 與 OS。

## 3. 原型實驗結果 (Prototype)
我們於 `hw_ecp_sim.py` 進行了硬體級別的調度模擬：
*   **基準測試 (軟體 OS 調度):** 每層 500us 額外開銷。
*   **HW-ECP (硬體自主調度):** 每層僅需 5us 設定開銷。
*   **效能提升:** 達成 **99.00% 的驅動程式開銷縮減**。

## 4. 硬體架構結論 (Conclusion)
 Edge NPU 必須具備「自主儲存管理 (Autonomous Storage Management)」能力。透過 HW-ECP，NPU 可以實現真正的 Zero-CPU MoE 推論，將原本浪費在 Context Switch 的時間完全轉化為有效的資料預取 (Prefetching) 寬限期。
