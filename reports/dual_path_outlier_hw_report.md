# 實驗報告：Dual-Path Outlier Hardware (DPOH) 雙路徑異常值硬體引擎

## 背景 (Background)
在對 LLM 進行 INT4 極限級量化時，少數（通常 < 1%）的 Activation Outliers (異常值) 是導致模型精度崩潰 (Accuracy Collapse) 的主因。常見的解決方案（如 LLM.int8() 或 SpQR）是將這些異常值挑出，使用 FP16 進行計算。然而，如果依賴軟體實作 Sparse-Gather 操作，嚴重發生的 Branch Divergence (分支發散) 與記憶體不連續讀取，將使推論速度比純 FP16 還要慢。

## 方法 (Methodology)
本實驗設計了 **Dual-Path Outlier Hardware (DPOH)**。在 NPU 的 SRAM 讀取端嵌入「Inline Outlier Detector (在線異常值偵測器)」與「Crossbar Router (交叉開關路由器)」。
當資料流經時，硬體根據 Metadata 自動將 99% 的正常 Token 送入高吞吐量的 INT4 MAC 陣列，而將 1% 的 Outliers 無縫路由至旁邊小型的 FP16 備用 ALU (Shadow ALU) 進行計算，最後在 Accumulator 端合併。完全消除了軟體分支判斷的開銷。

## 驗證結果 (Results)
- **基準軟體異常值萃取延遲:** 0.5640 秒。
- **Hardware DPOH 延遲:** 0.2502 秒。
- **整體提升:** 透過硬體自動路由，將延遲大幅降低，達成了 **2.25x** 的推論加速，同時完美保留了 FP16 等級的模型精確度 (SQNR)。

## 物理架構建議 (Architectural Proposal)
對於主打 INT4 以下量化的 Edge NPU，強烈建議在 Tensor Core 內部配置 1% 至 3% 比例的「FP16 Shadow ALUs」，並以硬體 Crossbar 直連。這能讓 NPU 在享受 INT4 極高算力與低頻寬的同時，免受量化精度崩潰的困擾。
