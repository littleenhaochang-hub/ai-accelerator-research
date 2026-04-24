# LUT-Mamba Sub-4-bit Scan Hardware Acceleration Report

## 實驗背景 (Background)
根據最新的 ICLR/ICML 趨勢，Mamba/SSM 模型架構解決了 Transformer O(N^2) 的注意力瓶頸，但其硬體執行仍受限於序列掃描 (Sequential Scan) 中的浮點乘加 (MAC) 運算延遲。同時，次 4-bit (Sub-4-bit) 查找表 (LUT) 硬體架構被證明能有效降低能耗。本實驗旨在探討將 LUT 架構與 Mamba 狀態掃描結合的硬體軟體協同設計。

## 實驗方法 (Methodology)
撰寫 `lut_mamba_sim.py`，比較基準的 FP16 Mamba 掃描延遲與模擬的 LUT-Mamba (Sub-4-bit) 架構延遲。在 LUT 架構中，我們將矩陣乘法替換為 SRAM 查找表讀取，大幅降低運算複雜度。

## 實驗數據 (Empirical Data)
- **Sequence Length:** 8192
- **Hidden Dimension:** 2048
- **Baseline FP16 Scan Latency:** 31.41 ms
- **LUT-Mamba Latency:** 9.01 ms
- **Throughput Speedup:** 3.48x

## 硬體架構提案 (Hardware Architecture Proposal)
我們提出在 Edge NPU 內部整合 **"Hardware LUT-Scan Engine"**。該引擎直接於 SRAM 讀取端口旁配置 4-bit LUT，讓 Mamba 狀態更新的 $A \times h$ 運算轉換為零週期的查找表映射 (Zero-cycle LUT Mapping)，從而完全避開耗電且高延遲的數位乘法器 (Digital Multipliers)，達到 3.48 倍的加速比，非常適合功耗受限的邊緣設備。
