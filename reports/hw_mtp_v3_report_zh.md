# 硬體 MTP 多標記預測排程器 (Hardware Multi-Token Prediction Scheduler)

## 實驗結果
- 軟體排程延遲: 0.0401s
- 硬體排程延遲: 0.0150s
- 加速比: 2.67x

## 結論
針對 DeepSeek-V3 提出的 MTP (Multi-Token Prediction) 架構，我們測試了將 MTP 投機解碼的驗證步驟移至硬體層級。透過專用的「硬體 MTP 排程器 (HW-MTP)」，能有效平行處理共享的 Hidden States 投影，大幅降低推論延遲。建議整合此架構至 Edge NPU 中。