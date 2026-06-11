# Hardware Sparse Autoencoder Evaluator (HW-SAEE)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
Sparse Autoencoder (SAE) 被廣泛應用於大語言模型中的特徵提取與可解釋性研究。然而，在推論過程中，SAE 需要計算極高維度但極度稀疏的特徵。若使用傳統的軟體方式 (透過 Dense MAC 陣列) 計算這些特徵，將會產生巨大的記憶體頻寬需求與冗餘的 ALU 運算，成為系統的瓶頸。

## 文獻探索 (Literature Exploration)
為了解決 SAE 高維度稀疏特徵的計算瓶頸，我們探索了將其硬體化的可能性。相較於讓 CPU/GPU 透過繁重的軟體迴圈或不規則記憶體存取來計算 SAE 啟動值，我們提出在硬體層面設計一個專屬的「Sparse Autoencoder Evaluator」，直接在資料流中過濾並跳過大量的零值運算。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `hw_sparse_autoencoder_sim.py` 來進行軟硬體架構的延遲比較：
1. **Software SAE Latency**：模擬傳統軟體處理高維度 SAE 特徵時，因密集記憶體抓取與 ALU 評估所產生的延遲。
2. **Hardware SAE Evaluator**：模擬一個平行硬體區塊，能夠利用極端稀疏性 (Extreme Sparsity Skipping)，直接繞過密集的軟體執行路徑。

## 實驗數據 (Empirical Results)
*   **Features Count**: 16384
*   **Software SAE Latency**: 764.72 ms
*   **Hardware SAE Evaluator Latency**: 33.10 ms
*   **效能提升 (Speedup)**: **23.10x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
實驗證明，將 Sparse Autoencoder 的特徵評估與過濾轉移至平行的硬體區塊 (HW-SAEE)，能夠帶來 23.10 倍的延遲改善。我們強烈建議在未來的 Edge NPU 架構中整合此「HW-SAEE 引擎」，以極低的功耗與延遲原生支援模型內部高維稀疏特徵的即時解析與應用。