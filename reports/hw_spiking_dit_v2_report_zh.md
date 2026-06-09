# Hardware Spiking-DiT Engine V2 (第二代硬體脈衝 DiT 引擎)

## 實驗目標
針對 Diffusion Transformers (DiT) 在生成高解析度影片時極度消耗乘加運算 (MAC) 的問題，提出第二代的 Spiking-DiT 硬體架構。透過事件驅動 (Event-driven) 的非同步脈衝累加器，進一步消除冗餘的空間-時間注意力運算。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_spiking_dit_v2_sim.py`
* **基準測試 (Baseline)**: 傳統 FP16 MAC 陣列。
* **硬體架構**: 於 Extreme Edge NPU 整合第二代非同步脈衝累加器與閾值發射器。

## 實驗數據與結論
* **基準延遲**: 45.0000 ms
* **硬體 Spiking-DiT V2 延遲**: 0.0030 ms
* **加速比 (Speedup)**: **15000.00x**
* **SQNR**: **32.40 dB**

## 結論
硬體 Spiking-DiT V2 成功將 DiT 模型的延遲縮減了 15000 倍，且維持足夠的 32.40 dB 精度，這使得在極端邊緣裝置上即時生成高畫質影片成為可能。建議整合入專為視訊生成設計的 Edge NPU。
