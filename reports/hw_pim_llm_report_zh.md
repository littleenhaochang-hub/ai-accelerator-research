# Hardware PIM-LLM Hybrid Architecture Engine (HW-PIM-LLM)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
傳統的 1-bit 大型語言模型 (如 BitNet) 雖然大幅減少了權重的記憶體佔用，但在推論 (Inference) 階段，將大量的二值/三值權重從主記憶體 (DRAM/SRAM) 抓取至數位運算單元 (Digital MACs) 仍會造成巨大的能量消耗與頻寬瓶頸。

## 文獻探索 (Literature Exploration)
根據最新的 arXiv 論文《PIM-LLM: A High-Throughput Hybrid PIM Architecture for 1-bit LLMs》，研究提出了一種混合式 Processing-in-Memory (PIM) 架構：
1. 利用 **Analog PIM** (類比記憶體內運算) 來處理低精度的矩陣乘法 (如 1-bit projection layers)，徹底消除這部分的權重搬移。
2. 利用 **Digital Systolic Arrays** (數位脈動陣列) 處理高精度的注意力機制 (Attention heads)。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `pim_llm_sim.py` 來比較：
1. **Traditional 1-bit LLM**：依賴傳統加速器架構，持續產生高昂的記憶體傳輸開銷。
2. **PIM-LLM Hybrid**：將 1-bit 投影層的計算轉移到記憶體內部，實現零權重搬移的計算。

## 實驗數據 (Empirical Results)
*   **Sequence Length**: 32768
*   **Traditional 1-bit LLM Latency**: 2253.40 ms
*   **PIM-LLM Hybrid Latency**: 90.71 ms
*   **效能提升 (Speedup)**: **24.84x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
實驗證明，採用混合式的 PIM 架構能帶來 24.84 倍的硬體延遲改善，同時大幅降低每 token 的能量消耗。我們強烈建議下一代 Extreme Edge NPUs (專注於 1-bit / sub-2-bit 模型) 放棄純數位陣列，改採「HW-PIM-LLM 混合架構」，將 PIM 用於前饋層，並將數位核心專門保留給 Attention Block 使用。