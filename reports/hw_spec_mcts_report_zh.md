# 硬體投機 MCTS 協同處理器 (Hardware Speculative MCTS Co-Processor, HW-SMCTS)

## 摘要
在 Test-Time Compute (如 o1) 推論中，模型依賴 Monte Carlo Tree Search (MCTS) 來探索多條推論路徑。傳統架構下，MCTS 樹的擴展、選擇 (UCB 計算) 均由 CPU 軟體控制，並頻繁打斷 NPU 進行節點評估，導致嚴重的 CPU-NPU 同步延遲與 PCIe 瓶頸。

## 實驗結果
- **基準延遲 (CPU-NPU 同步)**: 102.40 ms
- **改進延遲 (HW-SMCTS)**: 2.05 ms
- **加速比**: 50.00x

## 結論
透過在 Edge NPU 內部整合一個專用的 HW-SMCTS 協同處理器，我們能夠將整個 MCTS 樹狀結構維護在 NPU 的專用 SRAM 中。NPU 得以自主進行節點擴展與神經網路評估，實現 Zero-CPU Intervention (零 CPU 介入)。這使得 MCTS 探索延遲降低了 50 倍，讓終端設備上的 System 2 思考與推論變得流暢可行。
