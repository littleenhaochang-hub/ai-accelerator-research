# Auto-Researcher 分析報告：Hardware Speculative Mamba (HSM)

## 實驗背景
State Space Models (如 Mamba) 雖然在長文本上具有優勢，但其序列相依性 (Sequential Dependency) 導致在 Decode 階段無法像 Transformer 一樣利用 KV Cache 進行平行計算。

## 解決方案 (HSM)
我們提出並模擬了 **硬體推測性 Mamba (HSM)** 架構。
整合一個輕量級的「Hardware Draft State Tracker」，在硬體層面快速預測未來幾個 step 的 Mamba hidden state，隨後交由主 Tensor Core 陣列進行平行驗證 (Parallel Verification)，將原本的序列相依性打破。

## 模擬數據 (hw_speculative_mamba_sim.py)
* **Baseline Latency (Sequential)**: 55.00 ms
* **HSM Latency (Speculative)**: 16.50 ms
* **Throughput Speedup**: 3.33x

## 架構建議
建議在 Edge NPU 內部增設「Mamba 狀態推測器 (Draft State Tracker)」與「平行驗證器」，原生支援 Mamba 架構的 Speculative Decoding，以達到極限的生成速度。