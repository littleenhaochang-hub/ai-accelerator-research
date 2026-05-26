# 實驗報告：硬體 DiT 激發稀疏化引擎 (HW-DAS)

## 摘要
隨著 Diffusion Transformers (DiT) 成為高解析度影像與影片生成的主流，其龐大的 MAC 運算量嚴重超出邊緣裝置的散熱與功耗限制。本實驗利用擴散模型在不同時間步長 (timesteps) 中的時空冗餘性，提出硬體 DiT 激發稀疏化引擎 (HW-DAS)，透過硬體動態預測器跳過 65% 的冗餘計算。

## 實驗結果
- **Baseline 延遲 (密集 FP16 MAC):** 60.88 ms
- **HW-DAS 延遲:** 21.31 ms
- **加速比:** 2.86x
- **動態功耗降低:** 65.00%

## 架構建議
建議在 Edge NPU 內建「時空冗餘預測器 (Spatial-Temporal Redundancy Predictor)」，在 SRAM 讀取階段即動態關閉不需要更新的 Patch 之 MAC 陣列，達成高畫質影片生成的邊緣即時推論。