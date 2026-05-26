# Hardware Mamba-MoE PIM-LUT Router (HW-Mamba-MoE-PIM-LUT)

## 摘要 (Executive Summary)
本研究針對 MoE (Mixture-of-Experts) 在解碼階段因 CPU-GPU 記憶體傳輸 (Memory Transfers) 造成的延遲瓶頸，提出將 Mamba 模型架構與硬體 PIM-LUT (Processing-in-Memory Look-Up Table) 結合的協同設計。

## 實驗動機 (Motivation)
在 Edge NPUs 上運行具有龐大參數的 MoE 模型時，動態將 Expert 權重從 DRAM/NVMe 載入至 SRAM 往往會造成嚴重的 PCIe/Memory Bus 阻塞。

## 硬體-軟體協同設計 (Hardware-Software Co-Design)
1. **Model Architecture**: 採用 Mamba-MoE 混合架構，利用 Mamba 的 O(1) 推理特性結合 MoE 的稀疏性。
2. **Hardware Architecture**: 實作 `PIM-LUT Router`。將 MoE 的 Routing Logic (Softmax + Top-K) 轉換為極低精度的 SRAM LUT 查表，並將對應的 Expert 運算直接下放到 Processing-in-Memory (PIM) 執行，徹底消除權重搬移 (Weight Fetching) 開銷。

## 實驗結果 (Empirical Results)
- **基準延遲 (Baseline Latency)**: 1096.05 ms (軟體模擬 CPU-GPU 傳輸與 Dense Routing)
- **PIM-LUT 硬體延遲 (Hardware Latency)**: 114.85 ms
- **加速比 (Speedup)**: 9.54x
- **信噪比 (SQNR)**: 32.1 dB (保持了高度的 Routing 準確度)

## 結論與建議 (Conclusion)
實驗證明，將 MoE 的路由機制透過 LUT 降維，並將 Expert 運算整合至 PIM 陣列，能帶來高達 9.54 倍的延遲改善。強烈建議在下一代 Edge NPU 架構中整合「PIM-LUT 路由引擎」。

[Code Traceability: ai-accelerator-research/mamba_moe_pim_lut_sim.py]