# FlashAttention-3 Async Hardware Overlap Report
## 背景 (Background)
FlashAttention-3 強調 Warp-Specialization 與 Async TMA (Tensor Memory Accelerator) 來隱藏記憶體載入延遲。對於 Edge NPU，這等同於在 SRAM 之間實作 Ping-Pong Buffering，讓 DMA 與 MAC 單元完全解耦。

## 模擬參數 (Parameters)
- Sequence Length: 8192
- Block Size: 128
- SRAM Bandwidth: 2000 GB/s
- NPU Compute: 20.0 TOPS

## 模擬結果 (Results)
- TMA Block 載入延遲: 0.0492 µs
- MAC Block 計算延遲: 0.2097 µs
- 循序執行總延遲: 16.57 µs
- 異步重疊執行總延遲: 13.47 µs
- 理論硬體加速比: 1.23x

## 架構建議 (Architectural Proposal)
新一代 Edge NPU 必須配備**獨立的 Async DMA 引擎**與**雙緩衝 SRAM 架構 (Ping-Pong SRAM)**。當 MAC 單元正在計算第 N 個 Block 的 $QK^T$ 時，DMA 引擎應在背景非同步載入第 N+1 個 Block 的 K/V 權重，完全隱藏記憶體牆的存取延遲，使系統達到 100% 的 Compute-Bound 狀態。
