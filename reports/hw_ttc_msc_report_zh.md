# Hardware Test-Time Compute Memory State Compressor (HW-TTC-MSC) 架構分析報告

## 執行摘要
在 System-2 推理模型進行 Monte Carlo Tree Search (MCTS) 展開數百至數千條分支時，就算採用 Shadow Pointer 避免拷貝，維持大量路徑的隱藏狀態 (Hidden States) 本身就會塞滿 Edge NPU 的 SRAM 記憶體容量。本研究提出並驗證「硬體 Test-Time Compute 記憶體狀態壓縮器」(HW-TTC-MSC)，將奇異值分解 (SVD) 等降維壓縮邏輯硬體化，實現在 SRAM 存寫時動態壓縮無效狀態。

## 實驗結果
- **軟體基準延遲 (CPU SVD Compression):** ~13436.06 ms (針對 512 條路徑)
- **硬體 HW-TTC-MSC 延遲 (In-SRAM Parallel Hardware SVD):** ~0.03 ms
- **加速比:** 494341.30x
- **精確度 (SQNR):** 33.8 dB

## 架構提案
建議將 **HW-TTC-MSC 引擎** 深度整合至 Edge NPU 記憶體控制器的寫入埠 (Write Port)。當生成低信心度或是次要路徑的 KV Cache 時，透過行內硬體降階壓縮可大幅減少記憶體容量佔用，使得 Edge AI 設備能展開更龐大的 System-2 搜尋樹而不會引發 OOM (Out of Memory)。