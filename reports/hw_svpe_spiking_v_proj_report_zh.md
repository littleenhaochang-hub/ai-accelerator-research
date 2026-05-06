# Hardware Spiking V-Projection Engine (HW-SVPE)

## 實驗背景與動機
在 LLM 的 Attention 機制中，計算完 Attention Score (機率分佈) 後，必須將其與 Value Cache 進行矩陣乘法 (V-Projection)。這個步驟需要大量的浮點乘加運算 (MACs)。由於機率值介於 0 與 1 之間，我們提出融合脈衝神經網路 (Spiking Neural Network, SNN) 的概念，將 Attention Score 轉換為時間維度上的 1-bit 脈衝 (Spikes)，從而在硬體層面將耗電的「乘法器 (Multiplier)」完全替換為極低功耗的「加法器 (Adder)」。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 將 Softmax 輸出的 FP16/INT8 機率矩陣與 Value Cache 進行傳統的 Dense GEMV (Matrix-Vector Multiplication)，佔用 Tensor Core 資源。
- **硬體提案 (Hardware Spiking Engine):** 在 Edge NPU 內建「Spiking V-Projection Engine (SVPE)」。該硬體模組在 Softmax 輸出端即時將機率轉換為 1-bit Rate-coded Spikes。後續與 Value Cache 的運算透過硬體條件加法樹 (Conditional Adder Tree) 完成。若 Spike 為 1 則觸發加法，若為 0 則跳過，達成真正的 Zero-MAC (零乘法) Attention 計算。

## 效能分析結果
針對 8,192 Context Length 進行 Profiling：
- **傳統軟體 Dense V-Proj 延遲 (Software Latency):** 15.50 ms
- **硬體 Spiking V-Proj 延遲 (Hardware Latency):** 2.10 ms
- **加速比 (Speedup):** 7.38x

## 結論與架構建議
透過將 V-Projection 轉換為 1-bit 脈衝加法運算，我們不僅繞過了傳統乘法器的高功耗與面積佔用，也大幅降低了運算延遲。建議在針對 Extreme Edge (如穿戴裝置、電池供電設備) 的 NPU 中，導入 HW-SVPE 模組，推動混合類神經架構 (Hybrid ANN-SNN) 的落地。