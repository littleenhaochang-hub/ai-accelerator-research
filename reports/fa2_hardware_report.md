# FlashAttention-2 SRAM I/O 硬體架構驗證報告

## 執行摘要
FlashAttention-2 (FA2) 透過重構 Attention 的計算順序，將大部分的 Rescaling (重新縮放) 運算延遲到迴圈的最後，並盡可能將中間狀態 (O matrix 與 softmax 統計量) 保持在暫存器 (Registers) 中。本實驗從硬體層面的 SRAM 讀寫次數，驗證 FA2 對於 Edge NPU 的頻寬釋放效益。

## 實驗數據與分析
- **目標架構**: 8K Context (seq_len=8192), Head Dim 128, Block Size 64x64
- **SRAM 讀寫次數比較 (以 Elements 為單位)**:
  - FA1 讀取: 5.37e+08
  - FA1 寫入: 2.68e+08
  - FA2 讀取: 2.69e+08
  - FA2 寫入: 1.05e+06
- **硬體效能增益**:
  - SRAM 讀取次數減少: 1.99x (約 2 倍)
  - SRAM 寫入次數減少: 256.00x (大幅消滅中間狀態寫回)

## 硬體架構結論
1. **消滅 SRAM 寫入瓶頸**: FA2 最大的硬體價值在於它幾乎完全消滅了 Attention 內部迴圈的 SRAM 寫入動作 (減少 256 倍)。這對功耗與熱量極度敏感的 Edge NPU 來說是巨大的進步。
2. **協同設計提案**: FA2 的成功極度依賴暫存器 (Registers)。為了讓 FA2 在 Edge NPU 發揮最大效能，硬體架構師必須大幅擴充 Tensor Core 旁的「Accumulator Register Files (累加器暫存器陣列)」，確保能夠完整容納 Block_size_Q $\times$ Head_dim 的中間矩陣，否則 Register Spilling 會導致 FA2 效能直接退化回 FA1。
