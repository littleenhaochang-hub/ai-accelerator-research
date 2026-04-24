# 硬體架構研究報告：Sparse Attention Pattern Matching Hardware

## 1. 瓶頸分析
在長文本 (Long Context) 處理中，採用 Sparse Attention 可以大幅減少計算量。然而，軟體在決定哪些區塊需要計算時，需付出較高的比對成本，造成 CPU/NPU 的 Overhead。

## 2. 文獻與架構探討
本研究探討將稀疏模式比對 (Pattern Matching) 硬體化，直接在 SRAM 控制器旁整合 "Sparse Pattern Matcher"。

## 3. Prototype 驗證與數據
- **Software Overhead:** 0.51 ms
- **Hardware Overhead:** 0.01 ms
- **Throughput Speedup:** 40.00x

## 4. 硬體設計建議 (Hardware Proposal)
建議在 Edge NPU 整合 "Hardware Sparse Pattern Matcher"，以無延遲地跳過不需要的 Attention 區塊計算。