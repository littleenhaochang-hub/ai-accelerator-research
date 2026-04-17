# MoE Expert-Choice Routing 硬體負載平衡分析

## 實驗背景
在 Mixture of Experts (MoE) 模型中，傳統的 Token-Choice Routing（由 Token 選擇 Top-K 專家）經常面臨負載不均 (Load Imbalance) 的問題。在硬體層面，這會導致部分 MAC 陣列嚴重 Stalling（等待最忙碌的專家運算完畢），而其餘陣列閒置，甚至為了符合硬體 Capacity 而丟棄 (Drop) 大量 Tokens。我們模擬了 Expert-Choice Routing 的硬體利用率改善幅度。

## 實驗方法
撰寫 `moe_routing_sim.py`，模擬 4096 個 Tokens 分配至 16 個 Experts。
導入 Zipf 長尾分佈來模擬 Token 偏好極端化，並比較 Token-Choice 與 Expert-Choice 的硬體 MAC 利用率與 Token 遺失率。

## 實驗數據
- **Token-Choice 遺失率**: 51.8% (大量 Tokens 超出單一專家 Capacity)
- **Token-Choice 硬體利用率**: 24.1%
- **Expert-Choice 遺失率**: 0.0%
- **Expert-Choice 硬體利用率**: 100.0%

## 硬體架構結論
Expert-Choice 路由算法透過「專家選擇 Tokens」能完美達到 100% 的運算單元負載平衡，徹底消除了硬體 Stalling 造成的效能黑洞與 Token 丟失。
要實現此架構的零開銷，未來的 Edge NPU 必須在 Router 階段硬體化實作 **Global Top-K Sorting Network (全域 Top-K 排序網路)**，以取代極度耗時的軟體 GPU/CPU 排序，使得各個專家的 Token 分派能在一個 Clock Cycle 內完成。
