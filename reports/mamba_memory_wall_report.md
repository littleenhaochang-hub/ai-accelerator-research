# Mamba/SSM 邊緣硬體效能瓶頸分析：Associative Scan 的記憶體牆

## 背景
在 `ai-accelerator-research/RESEARCH_REPORT.md` 中，我們針對 Mamba 等 State Space Models (SSM) 進行分析。這類架構在理論上具有 $O(N)$ 的時間複雜度，被認為是取代 Transformer 的有力候選者。

## 物理極限與硬體模擬
我們撰寫了 `mamba_scan_sim.py` 來模擬硬體在執行 Parallel Associative Scan 時的 Compute (MAC) 與 Memory Bandwidth 消耗。測試結果顯示：
- **算術強度 (Arithmetic Intensity) 極低：** 在 100 TFLOPS 與 100 GB/s 的邊緣設備配置下，Compute Time 僅需 0.02ms，但 Memory Time 高達 100ms (Seq=32K)。算術強度趨近於 0.0002。
- **記憶體牆 (Memory Wall)：** 執行並行 Scan 需要在 SRAM 與 DRAM 之間大量搬移狀態矩陣 (A, B, C, $\Delta$)。在 131K 長度下，光是這些隱藏狀態的資料流就高達 40GB，超過 Mac mini 的 16GB 記憶體上限，直接導致頻寬枯竭與 OOM。

## 結論與硬體協同設計方案
Mamba 架構雖然消除了 $O(N^2)$ 的 Attention MAC 運算，卻將壓力轉移到了記憶體頻寬上 (Memory Bound)。未來的邊緣 NPU 必須設計專用的 **SRAM-based Scan 暫存器** 或引入 **Processing-in-Memory (PIM)**，將狀態更新(State Update)的計算直接下放至記憶體控制器內，避免巨大的資料搬移，否則 SSM 在長文本上的延遲優勢將被硬體頻寬完全抵銷。
