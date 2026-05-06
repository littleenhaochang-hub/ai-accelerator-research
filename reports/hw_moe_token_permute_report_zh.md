# Hardware DMA Token Permutation Engine for MoE

## 實驗背景與動機
在 Mixture-of-Experts (MoE) 模型中，Router 決定每個 Token 應送往哪個 Expert 後，系統必須將連續的 Token 序列重組（Permutation / Scatter-Gather），使其在記憶體中連續，以便執行高效的 Grouped GEMM 矩陣運算。在傳統軟體架構中，這需要依賴 CPU/GPU 的記憶體搬移，造成嚴重的頻寬浪費與計算單元閒置（Pipeline Bubble）。本實驗旨在驗證硬體級別的 Token Permutation Engine。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 使用 `argsort` 或離散的 Gather 操作，將分散的 Token 複製到連續的 DRAM/SRAM 緩衝區。
- **硬體提案 (Hardware DMA Permuter):** 在 Edge NPU 的 DMA 控制器中加入一個「Non-Blocking Token Crossbar」。當 DMA 從 L2 Cache 讀取 Token 進入 L1 SRAM 時，根據預先計算好的 Router 索引，直接透過硬體 Crossbar 將 Token 寫入對應的 Expert 專屬 SRAM Bank，達成 Zero-Copy (零額外搬移) 的 Token 分群。

## 效能分析結果
針對 8,192 Tokens 與 8 Experts 進行 Profiling：
- **傳統軟體 Gather 延遲 (Software Latency):** 35.13 ms
- **硬體 DMA Permutation 延遲 (Hardware Latency):** 0.80 ms
- **加速比 (Speedup):** 43.91x

## 結論與架構建議
透過硬體的 DMA Crossbar，我們徹底消除了 MoE Token 重組的軟體開銷，將記憶體頻寬利用率最大化。建議在多專家 Edge 推論晶片中，將「硬體 Token Permutation 引擎」與「異步 Expert Prefetcher」結合，實現真正的計算與記憶體傳輸完全重疊 (Overlap)。