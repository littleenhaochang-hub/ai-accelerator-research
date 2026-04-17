# SpikeGPT / SNN (脈衝神經網路) 硬體加速分析

## 實驗背景
為了追求極致的邊緣設備 (Edge Device) 節能推論，我們探索了基於 Spiking Neural Network (SNN) 的大型語言模型架構 (如 SpikeGPT)。SNN 的特點在於啟動值為二值化脈衝 (Binary Spikes) `{0, 1}`，這使得原本耗電的乘加運算 (MAC) 可以退化為單純的加法運算 (Accumulate, AC)，並帶來極高的激勵稀疏性 (Activation Sparsity)。

## 實驗方法
撰寫 `snn_spikegpt_sim.py` 腳本，模擬 2048 Context Length 下，傳統 Dense LLM 與 SpikeGPT 的硬體功耗差異。我們假設 FP16 MAC 功耗為 1.5 pJ，FP16 加法為 0.1 pJ，且 SNN 的平均觸發率 (Firing Rate) 為 15%。

## 實驗數據
- **Baseline Dense MAC Energy**: 51539.61 uJ
- **SpikeGPT (AC only, 15% rate) Energy**: 515.40 uJ
- **Energy Reduction**: 99.00%

## 硬體架構結論
透過將耗電的乘加運算轉為稀疏的加法運算，SNN 架構能為 LLM 推論帶來高達 **99.00% 的運算功耗縮減**。
為了解鎖這個神經形態計算 (Neuromorphic Computing) 的潛力，Edge NPU 不能繼續使用傳統的密集矩陣運算單元 (Dense Systolic Arrays)。我們必須在硬體中整合 **Asynchronous Spike Router (非同步脈衝路由器)** 與 **Add-only ALUs (純加法算術邏輯單元)**，讓硬體能以事件驅動 (Event-driven) 的方式運作，徹底發揮脈衝稀疏性帶來的 PPA (Power, Performance, Area) 終極優勢。
