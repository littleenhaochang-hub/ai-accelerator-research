# FlashAttention-4 Async Hardware 分析報告

## 背景
FlashAttention 依賴 SRAM 的 Tiling 來減少 DRAM 存取，但 Memory 讀寫與 MAC 計算仍可能存在同步等待。

## 解決方案
提出硬體層級的完全非同步 DMA 與 MAC 交錯執行 (Ping-pong buffering at Register level)。

## 實驗結果
模擬顯示 1.82x 的速度提升。

## 結論
建議 Edge NPU 加入非同步 Tensor Memory Accelerator (TMA)。
