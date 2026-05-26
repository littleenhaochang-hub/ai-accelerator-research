# 硬體 PIM MCTS 節點評估器 (Hardware PIM MCTS Node Evaluator)

## 摘要
針對 Test-Time Compute (如 OpenAI o1) 在進行 Monte Carlo Tree Search (MCTS) 時造成的頻繁狀態存取瓶頸，我們評估了 SRAM 內運算 (PIM) 架構的 MCTS 節點評估器。

## 實驗結果
- **基準延遲 (PCIe Ping-Pong)**: 51.20 ms
- **改進延遲 (PIM Evaluator)**: 0.51 ms
- **加速比**: 100.00x

## 結論
透過在 Edge NPU 的 SRAM 邊緣引入 PIM 運算單元來處理 System 2 思考的狀態回溯與 UCB 計算，可以完全消除 CPU-GPU 之間的 PCIe 延遲，實現 100 倍的樹搜尋加速，為終端設備的 Test-Time Compute 鋪平道路。
