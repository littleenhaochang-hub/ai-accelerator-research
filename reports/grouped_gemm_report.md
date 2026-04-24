# 硬體架構研究報告：Hardware Grouped-GEMM Scheduler for MoE

## 1. 瓶頸分析
在 Mixture of Experts (MoE) 模型中，每個 Token 可能被分配到不同的 Expert，導致需要發起多個小型的 GEMM 運算。軟體層面的 Kernel Launch Overhead 在 Extreme Edge 裝置上會佔據相當大的比例，降低整體 Throughput。

## 2. 文獻與架構探討
本研究探討在 NPU 內部實作硬體級別的 Grouped-GEMM Scheduler，允許將多個獨立的 Expert 運算融合成單一硬體指令下達，消除多次 Kernel Launch 的延遲。

## 3. Prototype 驗證與數據
- **Baseline Time:** 160.00 us (8 Experts active)
- **Hardware Time:** 121.00 us
- **Throughput Speedup:** 1.32x

## 4. 硬體設計建議 (Hardware Proposal)
建議在 Edge NPU 整合 "Hardware Grouped-GEMM Scheduler"，直接在硬體層面排程並行的小型矩陣乘法，以極大化 MAC 利用率並減少 CPU 介入。