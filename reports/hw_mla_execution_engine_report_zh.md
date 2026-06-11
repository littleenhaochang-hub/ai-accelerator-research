# Hardware MLA Execution Engine (HW-MLA-EE)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
DeepSeek-V2/V3 引入的 Multi-Head Latent Attention (MLA) 將 Query, Key, 與 Value 投影到低維潛在空間 (latent space)，從而大幅縮小 KV-cache 並降低自迴歸解碼時的記憶體頻寬需求。然而，在資源受限的 Edge NPU 上，潛在投影矩陣 (latent projection matrices) 的執行策略 (執行重用 reusing vs 動態重算 recomputing) 對於硬體管線的吞吐量有決定性的影響。

## 文獻探索 (Literature Exploration)
根據最新論文《Hardware-Centric Analysis of DeepSeek's Multi-Head Latent Attention》，研究者指出在執行 MLA 時，可選擇「重用 (Reusing) 投影矩陣」或「動態重算 (Recomputing) 投影矩陣」。在頻寬受限的硬體平台上，動態重算可以將原本 Memory-Bound 的注意力工作負載轉移到 Compute-Bound 領域，從而利用充裕的數位 MAC 算力掩蓋記憶體瓶頸。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `mla_execution_sim.py`，比較在 Edge NPU 上的兩種 MLA 執行策略：
1. **MLA Reusing (Bandwidth Bound)**：重用展開後的投影矩陣，消耗大量內部 SRAM 頻寬。
2. **MLA Recomputing (Compute Bound)**：在硬體層面即時重算投影，增加 MAC 運算量但大幅削減記憶體存取。

## 實驗數據 (Empirical Results)
*   **Sequence Length**: 32768
*   **MLA Reusing Latency**: 2273.06 ms
*   **MLA Recomputing Latency**: 671.27 ms
*   **效能提升 (Speedup)**: **3.39x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
我們的實驗證明，在頻寬受限的 Edge NPU 上，採用硬體原生的「動態重算 (Recomputing)」策略能帶來高達 3.39 倍的延遲改善。我們強烈建議未來的 NPU 架構整合「HW-MLA 執行引擎 (HW-MLA-EE)」，並配備專用的張量核心管線來原生支援 DeepSeek MLA 的動態重算，以最大化硬體吞吐量。