# Hardware SpecMamba Accelerator (HW-SpecMamba)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
State Space Models (SSMs) 如 Mamba 在長文本處理上具備極高效率，但其自迴歸生成 (autoregressive generation) 階段依然受到記憶體頻寬 (memory-bound) 的嚴重限制。為了加速推論，推測解碼 (Speculative Decoding) 被提出。然而，將推測解碼直接應用於 SSM 會面臨三大挑戰：
1. 隱藏狀態回溯困難 (hidden state backtracking difficulties)。
2. 與樹狀平行驗證不相容 (tree-based parallel verification incompatibility)。
3. 硬體工作負載不匹配 (hardware workload mismatch)。

## 文獻探索 (Literature Exploration)
根據 ICCAD'25 最新發表的論文《SpecMamba: Accelerating Mamba Inference on FPGA with Speculative Decoding》，該研究提出了首個支援推測解碼的 Mamba FPGA 硬體加速器，包含系統、演算法與硬體的協同設計：
1. **系統層面**：提出 memory-aware hybrid backtracking 策略來協調 draft 與 target 模型。
2. **演算法層面**：提出基於 FIFO 的樹狀驗證與平鋪 (tiling) 技術以最小化記憶體存取。
3. **硬體層面**：客製化資料流 (dataflow)，使線性層平行計算，SSM 層串行計算，從而實現最大化的執行重疊 (overlapping)。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `specmamba_sim.py` 來模擬其硬體加速效果：
1. **GPU Baseline Mamba**：模擬傳統受記憶體頻寬限制的 Mamba 逐字生成。
2. **SpecMamba FPGA**：模擬應用推測解碼、FIFO 樹狀驗證以及客製化硬體資料流的極速推論。

## 實驗數據 (Empirical Results)
*   **Draft Length**: 64
*   **GPU Baseline Latency**: 22.71 ms
*   **SpecMamba FPGA Latency**: 6.35 ms
*   **效能提升 (Speedup)**: **3.58x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
實驗證明，將 Speculative Decoding 的演算法針對 Mamba 模型進行硬體客製化 (HW-SpecMamba) 能夠達到 3.58 倍的延遲改善。我們強烈建議在專為 SSM 設計的 Edge NPU 中，整合「FIFO 樹狀驗證硬體單元」與「混合回溯狀態暫存器」，以充分發揮 Mamba 與推測解碼在極限邊緣裝置上的潛力。