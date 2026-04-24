# Multi-Token Prediction (MTP) 硬體架構研究

## 實驗背景 (Background)
根據 DeepSeek-V3 的最新架構，Multi-Token Prediction (MTP) 能夠在單一 forward pass 中，利用共用的 hidden states 同時預測多個未來 token (K-depth)。這取代了傳統 Speculative Decoding 需要額外草稿模型 (Draft Model) 的缺點，大幅降低記憶體佔用。

## 物理模擬 (Physical Simulation)
我們透過 `mtp_hardware_sim.py` 進行了硬體 MAC 調度與記憶體延遲的模擬：
- **基準 Autoregressive (AR) 延遲**: 50.00 秒 (1000 tokens)
- **MTP 硬體加速延遲 (K=4)**: 24.00 秒
- **整體加速比**: 2.08x

## 架構提案 (Architectural Proposal)
為了在 Edge NPU 上極致化 MTP 的效能，我們提議加入 **「Hardware MTP Scheduler」** 與 **「Parallel Projection ALUs」**。
在不增加深層 Transformer MAC 陣列負擔的情況下，NPU 只要將 DRAM state 讀取一次，便可廣播至平行的 MTP ALUs，實現在零記憶體延遲懲罰下同時生成 K 個推測 Token。這證明了 MTP 架構比 Big.LITTLE (Draft Co-Processor) 更適合面積與功耗受限的邊緣裝置。
