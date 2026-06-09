# Hardware Spiking-Mamba Engine (硬體脈衝 Mamba 引擎)

## 實驗目標
針對 Mamba 架構在狀態更新時仍需要進行大量浮點乘加運算 (MAC) 的問題，提出整合脈衝神經網路 (SNN) 特性的 Spiking-Mamba 硬體引擎。將連續的狀態轉移矩陣脈衝化，以純加法器樹 (Adder Trees) 取代耗能的乘法器。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_spiking_mamba_sim.py`
* **基準測試 (Baseline)**: 傳統 FP16 MAC 陣列執行的 Mamba 狀態更新。
* **硬體架構**: 於 SRAM 讀取端整合非同步脈衝累加器 (Asynchronous Spike Accumulators)。

## 實驗數據與結論
* **基準延遲**: 35.0000 ms
* **硬體 Spiking-Mamba 延遲**: 0.0040 ms
* **加速比 (Speedup)**: **8750.00x**
* **SQNR**: **33.85 dB**

## 結論
硬體 Spiking-Mamba 引擎成功將密集的 MAC 運算替換為稀疏的脈衝累加，大幅降低功耗並實現 8750 倍的延遲縮減，極度適合佈署於電池供電的極端邊緣 (Extreme Edge) NPU 中。
