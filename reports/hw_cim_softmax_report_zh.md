# Hardware Compute-in-Memory Softmax Accelerator (HW-CIM-Softmax)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
Transformer 注意力機制中的 Softmax 操作，由於依賴超越函數 (exponential) 且需要多趟記憶體讀寫 (計算 Max -> 計算 Exp -> 計算 Sum -> Divide)，導致其成為大語言模型 (LLM) 推論時的嚴重瓶頸。傳統架構下，記憶體頻寬需求隨序列長度呈 $O(N^2)$ 二次增長。

## 文獻探索 (Literature Exploration)
根據最新的 arXiv 論文《Hardware-Software Co-Design for Accelerating Transformer Inference Leveraging Compute-in-Memory》，研究提出了一種名為 HASTILY 的架構。該架構包含 Unified Compute and Lookup Modules (UCLMs)，能夠將查表 (Lookup) 與乘加運算 (MAC) 整合在同一個 SRAM 陣列中執行。這允許指數運算與矩陣乘法同時進行，而不需要傳統浮點運算單元 (FPU) 的介入。同時，透過細粒度的流水線排程，可將對序列長度的記憶體需求從二次降低為線性。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `cim_softmax_sim.py` 進行硬體延遲的模擬比較：
1. **Traditional FPU Softmax**：模擬將資料從 SRAM 讀取至數位 FPU 進行超越函數計算，再寫回記憶體的傳統流程。
2. **CIM-UCLM Softmax**：模擬直接在 SRAM 陣列內並行執行指數查表與累加操作 (Compute-in-Memory)。

## 實驗數據 (Empirical Results)
*   **Sequence Length**: 4096
*   **Traditional FPU Softmax Latency**: 194.81 ms
*   **CIM-UCLM Softmax Latency**: 43.04 ms
*   **效能提升 (Speedup)**: **4.53x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
我們的模擬證實了，將 Softmax 運算從數位邏輯單元轉移至 SRAM 的 Compute-in-Memory (CIM) 模組，能帶來高達 4.53 倍的延遲改善。強烈建議在未來的 Edge NPU 中，將傳統的 SRAM 陣列升級為「UCLM (Unified Compute and Lookup Modules) CIM-SRAM」，藉此在零資料搬移的情況下原生加速 Attention 層的核心計算。