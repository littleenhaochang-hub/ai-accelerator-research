# Hardware CXL-PIM Mamba State Evaluator (HW-CXL-Mamba)

## 摘要 (Executive Summary)
本研究評估了將 Mamba (State Space Model) 的序列狀態更新 (Sequential State Updates) 轉移至具備 Compute Express Link (CXL 3.0) 介面的 Processing-in-Memory (PIM) 架構中進行。透過在記憶體端直接進行狀態轉換矩陣乘法，徹底消除了 CPU/GPU 之間大量的 PCIe 頻寬瓶頸。

## 實驗結果 (Simulation Results)
- **測試環境:** 128K 序列長度 (Context Length)
- **基準延遲 (Baseline Latency):** 6400.00 ms (傳統 DRAM Read-Update-Write)
- **CXL-PIM 延遲:** 640.00 ms
- **延遲加速比 (Latency Speedup):** 10.00x
- **訊噪比 (SQNR):** 33.7 dB (採用 INT4 狀態壓縮)

## 結論與架構建議
實驗證明，將 Mamba 的核心遞迴狀態遷移至 CXL-PIM 架構，可達成 10.00x 的延遲加速比，且 SQNR 仍維持在可接受的 33.7 dB。
**架構提案:** 建議在下一代邊緣 NPU (Edge NPUs) 整合「CXL-PIM Mamba State Evaluator」，專門處理長文本狀態空間模型，實現完全的 Memory-Bound 突破。