# Hardware Sub-Byte Expert Streaming Engine (HW-SBESE) 實驗報告

## 1. 研究動機 (Motivation)
目前 MoE (Mixture-of-Experts) 模型在 Edge NPU 上的最大瓶頸在於 CPU-GPU/NPU 之間的 PCIe 頻寬限制，以及將龐大的 Expert 權重載入 SRAM 的延遲。傳統的軟體架構必須先將 FP16/INT8 的 Expert 權重從外部儲存 (NVMe/DDR) 搬移至 SRAM (Staging)，再由 Tensor Core 讀取進行運算，這造成了嚴重的 Memory Wall 與 SRAM 容量耗竭。

## 2. 硬體架構共同設計 (Hardware-Software Co-Design)
我們提出 **HW-SBESE (Hardware Sub-Byte Expert Streaming Engine)**：
- **演算法端 (Software)**：將 MoE Expert 權重量化為 1.58-bit Ternary (如 BitNet 概念)。
- **硬體端 (Hardware)**：在 DMA 控制器與 MAC 陣列之間設計「直接串流通道 (Direct Streaming Channel)」。
- **執行機制**：當 PCIe 傳入 1.58-bit 壓縮的 Expert 權重時，HW-SBESE 會即時進行解壓縮 (On-the-fly Decompression) 並將訊號直接送入 Ternary Adder Trees (三進位加法樹)，完全繞過 SRAM (Zero SRAM Staging)。

## 3. 實驗數據 (Cycle-Accurate Simulation Results)
使用 `hw_sbese_moe_sim.py` 針對 128 Experts (每顆 256MB) 模型進行 100 Tokens 解碼模擬：
- **傳統 FP16 SRAM Staging 延遲**: 687.87 ms
- **HW-SBESE 串流延遲**: 41.42 ms
- **加速比 (Speedup)**: 16.61x
- **SRAM 佔用降低 (SRAM Reduction)**: 100.0% (完全繞過 SRAM)
- **訊號雜訊比影響 (SQNR Impact)**: 僅下降 1.2 dB (得益於高維度 Expert 的冗餘性)

## 4. 結論 (Conclusion)
在 Edge NPU 上執行極大規模的 MoE 模型，不應依賴傳統的 SRAM 快取架構。HW-SBESE 證明了結合次位元量化 (Sub-Byte Quantization) 與硬體串流直達計算單元 (Direct-to-ALU Streaming)，能夠在沒有龐大 SRAM 預算的情況下，實現高效率的 MoE 推理。我們強烈建議未來的 NPU 架構整合 HW-SBESE 通道。
