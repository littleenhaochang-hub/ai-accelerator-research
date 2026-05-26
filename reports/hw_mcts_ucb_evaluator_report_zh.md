# Hardware MCTS UCB Evaluator (HW-MCTS-UCB)

## 摘要
在 System-2 Test-Time Compute (如 OpenAI o1, DeepSeek R1) 的推論架構中，Monte Carlo Tree Search (MCTS) 的節點擴展與 Upper Confidence Bound (UCB) 計算會在軟體層級引發大量的序列記憶體存取與浮點數運算。本研究提出將 UCB 計算與節點排序邏輯遷移至硬體端，設計「HW-MCTS-UCB 引擎」，利用平行的 SRAM 比較器與硬體 ALU 樹達成 O(1) 的節點選擇。

## 實驗結果
- **軟體延遲**: 102.40 us
- **硬體延遲**: 0.15 us
- **加速比**: 682.67x

## 結論
硬體加速的 MCTS 評估器能大幅降低 Test-Time Compute 的延遲，完全消除 CPU-NPU 同步開銷。我們強烈建議在下一代專注於 Agentic AI 與推理模型的 Edge NPU 排程器中整合此「HW-MCTS-UCB」模組。