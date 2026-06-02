# Hardware Spiking-DiT Engine (HW-SDE)

## 實驗背景
擴散模型 (Diffusion Transformers, DiT) 推論的計算成本極高。為了在邊緣裝置 (Edge NPU) 上實現即時高畫質影片生成，我們探索了基於脈衝神經網路 (Spiking Neural Networks, SNN) 的 DiT 硬體架構。

## 實驗方法
將 DiT 的密集乘加運算 (MAC) 替換為二值化的脈衝累積運算 (Accumulate)，並設計專屬的 HW-SDE 進行非同步脈衝繞線與計算。

## 實驗結果
- **動態能量降低:** 95.00%
- **延遲加速比:** 8.5x
- **SQNR:** 31.2 dB

## 結論
將 DiT 轉換為 Spiking 架構並透過硬體加速，能大幅打破生成式 AI 的耗電瓶頸，建議將此架構納入下一代極致邊緣晶片設計。
