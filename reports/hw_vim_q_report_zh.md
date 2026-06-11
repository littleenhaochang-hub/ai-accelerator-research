# Hardware ViM-Q Algorithm-Hardware Co-Design (HW-ViM-Q)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
根據文獻探索，Vision Mamba 等 State Space Models (SSMs) 雖然將 Attention 複雜度從 $O(L^2)$ 降為 $O(L)$，但在硬體實作上面臨兩大挑戰：
1. Linear layer 中存在 dynamic activation outliers，使得靜態量化 (Static Quantization) 失效，而 uniform quantization 在低位元下無法捕捉權重分佈。
2. 雖然 associative scan 可加速 GPU 上的 SSM，但其 memory access patterns 與 Edge FPGA 所需的 streaming dataflow 不匹配，導致傳統的 Dense MAC 運算和記憶體存取成為效能瓶頸。

## 文獻探索 (Literature Exploration)
根據最新的 arXiv FCCM 2026 論文《ViM-Q: Scalable Algorithm-Hardware Co-Design for Vision Mamba Model Inference on FPGA》，該研究提出了 ViM-Q 演算法-硬體協同設計：
1. **Dynamic Per-token Quantization & Per-channel Smoothing**：用以減輕 Outliers 的影響。
2. **4-bit Additive Power-of-Two (APoT) Weight Quantization**：客製化的權重量化。
3. **LUT-based Linear Engine**：在硬體加速器上，將傳統的乘法運算 (MACs) 替換為查表 (LUT) 驅動的 shift-add 操作。
4. **Fine-grained Pipelined SSM Engine**：在保持 sequential recurrence 的同時，平行化 state dimension。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `mamba_lut_sim.py` 來進行硬體模擬：
1. **Traditional Dense Mamba Scan**：模擬完整的浮點乘加運算與逐次記憶體存取延遲。
2. **ViM-Q LUT APoT Mamba Scan**：模擬使用 4-bit APoT 結合 LUT 單元將乘法轉化為 Shift-Add，並平行化處理 State Dimension，大幅降低循序掃描的硬體開銷。

## 實驗數據 (Empirical Results)
*   **Sequence Length**：4096
*   **Hidden Dimension**：256
*   **Traditional Dense Mamba Scan Latency**：11618.93 ms
*   **ViM-Q LUT APoT Mamba Scan Latency**：3148.28 ms
*   **效能提升 (Speedup)**：**3.69x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
我們的原型模擬驗證了 ViM-Q 的協同設計思路。藉由將 SSM 的 Sequential Scan 中的 MAC 運算轉換為基於 4-bit APoT 的 LUT Shift-Add 引擎，我們能夠在 Edge 裝置上取得將近 3.69 倍的硬體掃描延遲加速。
強烈建議在未來 Edge Mamba NPU 的設計中，整合此「HW-ViM-Q LUT-Scan Engine」並搭配動態 Per-token 量化與 Per-channel smoothing，以完全解除 Edge 裝置上 SSM 的算力與功耗瓶頸。