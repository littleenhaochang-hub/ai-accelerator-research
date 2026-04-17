# AWQ (W4A16) 即時反量化硬體架構分析

## 實驗背景
對於 Edge NPU，LLM 推論通常處於 Memory-Bound (記憶體頻寬受限) 的狀態。AWQ (Activation-aware Weight Quantization) 透過將權重量化為 4-bit，並保持激勵值為 16-bit (W4A16)，能大幅降低 DRAM 讀取量。然而，NPU 的核心通常是 FP16 MAC 陣列，因此權重在進入運算單元前必須被即時反量化 (Dequantization)。

## 實驗方法
撰寫 `awq_dequant_sim.py`，模擬 7B 參數模型在 W16A16 與 W4A16 (Group Size = 128) 下的記憶體佔用與頻寬延遲，並評估反量化管道的硬體需求。

## 實驗數據
- **Baseline W16 Weight Size**: 14.00 GB
- **AWQ W4 Weight Size**: 3.72 GB
- **Memory Footprint/Bandwidth Reduction**: 73.44%
- **Load Time (100 GB/s)**: 從 140.00 ms 降至 37.19 ms

## 硬體架構結論
W4A16 能夠節省 73.44% 的記憶體頻寬，是解鎖 7B 模型在邊緣裝置高速推論的關鍵。
要在硬體層面達到零延遲，Edge NPU 不能依賴 Tensor Core 本身來做反量化，而是必須在 SRAM 的讀取埠 (Read Ports) 與 MAC 陣列之間，安插專屬的 **On-the-fly Dequantization Pipeline (ODP, 即時反量化流水線)**。該模組需具備低功耗的 INT4 轉 FP16 查表單元與 FP16 加乘法器 ($w \times scale + zero$)，以確保 MAC 陣列能無縫接收標準浮點數。
