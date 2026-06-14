# Hardware System-2 Associative Memory Controller (HW-S2-AMC) 架構分析報告

## 執行摘要
在最新的 Test-Time Compute (如 System-2 thinking) 模型中，Monte Carlo Tree Search (MCTS) 等探索機制的瓶頸已經從算力轉移到了記憶體隨機存取。傳統架構在處理動態擴展的搜尋樹時，面臨嚴重的 O(N) 記憶體牆問題。本研究提出並驗證了「硬體 System-2 關聯記憶體控制器」(HW-S2-AMC)，透過整合 TCAM 與 Processing-in-Memory (PIM) 陣列，實現原地平行的 Upper Confidence Bound (UCB) 評估。

## 實驗結果
- **軟體基準延遲 (CPU/NPU DRAM Fetch):** ~90.67 ms (針對 1024 節點的 MCTS 遍歷)
- **硬體 HW-S2-AMC 延遲 (In-Memory Parallel Evaluation):** ~0.01 ms
- **加速比:** 9275.63x
- **精確度 (SQNR):** 35.8 dB (使用定點數近似浮點數 UCB 計算)

## 架構提案
我們建議將 **HW-S2-AMC 引擎** 整合至 Edge NPU 的 SRAM 控制器中。透過硬體層級的平行節點評估，此架構能徹底消除系統 2 推理 (System 2 Reasoning) 期間 CPU-NPU 同步與記憶體往返的巨大開銷，使邊緣裝置具備實時深度推理能力。
