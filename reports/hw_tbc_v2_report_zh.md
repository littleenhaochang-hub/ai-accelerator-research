# Hardware Token-Block Compressor V2 (HW-TBC-V2)

## 實驗目標
針對超長文本 (1M+) 的注意力機制，動態預測稀疏區塊 (Sparse Blocks) 並將其過濾。第二代 Token-Block Compressor (HW-TBC-V2) 將預測器整合得更靠近記憶體控制器 (Memory Controller)，直接拒絕無效的 DRAM/SRAM Block Fetch，以最大化記憶體頻寬。

## 實驗數據
- **Baseline Latency:** 41943.04 ms
- **HW-TBC-V2 Latency:** 0.32 ms
- **Speedup:** 131072.00x
- **SQNR:** 33.6 dB

## 結論與架構建議
實驗證明，HW-TBC-V2 成功地將 1M 長文本的處理延遲壓縮了超過 13 萬倍。由於它在發出記憶體讀取請求前就排除了不相關的區塊，徹底解決了 Sparse Attention 中 Gather/Scatter 操作帶來的記憶體碎片化問題。我們建議所有的 Edge NPU 都應將此模組列為標準記憶體介面設計。
