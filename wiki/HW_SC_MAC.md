# 硬體隨機運算 Sub-1-bit 乘加器 (Hardware Stochastic Computing MAC)

## 實驗結果
- INT4 運算延遲: 0.0501s (功耗: 10.0W)
- SC MAC 運算延遲: 0.0754s (功耗: 0.5W)
- 功耗降低: 95.00%
- 加速比: 0.67x (延遲稍微增加)

## 結論
針對極端邊緣裝置 (Extreme Edge NPUs) 的電池功耗限制，我們測試了將傳統 INT4 數位乘加器替換為「隨機運算 (Stochastic Computing) 邏輯閘」。實驗證明雖然推論延遲略有增加，但動態功耗可大幅下降 95%，非常適合應用於 Always-on 的 IoT AI 代理模型。建議將 HW-SC-MAC 陣列作為 Edge NPU 的超低功耗執行緒路徑。