# Test-Time Compute (TTC) 的硬體分支開銷分析

## 背景
最近的模型 (如 O1) 引入了 Test-Time Compute (TTC) 的概念，在推論期間根據問題的難度動態展開運算 (Dynamic Branching 或 Early Exit)。我們在 `ai-accelerator-research/RESEARCH_REPORT.md` 的 Pillar 中探討了其對邊緣硬體架構的影響。

## 硬體模擬與分析
我們透過 `ttc_branching_sim.py` 模擬了在隱藏維度 4096 的模型上，動態啟用額外 16 層 (TTC Layers) 的硬體開銷：
- **運算與記憶體開銷：** TTC 層會帶來 50% 的 MACs 與記憶體空間 (約 6GB) 增長。
- **記憶體牆 (Memory Wall) 懲罰：** 在 Edge 設備 (Batch=1) 且頻寬為 100 GB/s 的情況下，如果 TTC 層未常駐在 SRAM/Cache 中，動態從 DRAM 載入權重會導致 **60ms/token 的極高延遲懲罰**。

## 結論與硬體優化方案
如果要在邊緣 NPU 上實現高效的 TTC Branching：
1. **權重無法 on-demand 載入：** 在 Batch=1 的情況下，動態分支的記憶體讀取延遲遠大於計算延遲。
2. **解決方案：SRAM Pinning 與 4-bit 量化。** 所有 TTC 相關的權重必須被強制量化至 4-bit (或更低，如 W2A4) 並常駐 (Pinned) 在 DRAM/SRAM 中。不應在推論時才進行 PCIe / UFS 到 DRAM 的權重搬移。未來的硬體應設計 **Power-Gated MACs**，在不需要 TTC 層時直接關閉電源，而不是將權重卸載至低速儲存中。
