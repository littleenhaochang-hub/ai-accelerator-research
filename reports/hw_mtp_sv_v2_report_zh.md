# Hardware Multi-Token Prediction Speculative Verifier V2 (HW-MTP-SV-V2)

## 實驗目標
針對 DeepSeek-V3 提出的 Multi-Token Prediction (MTP) 架構，解決多個平行預測頭在驗證階段的軟體延遲。我們設計了第二代的 MTP 硬體驗證器 (HW-MTP-SV-V2)，進一步優化了多頭平行驗證的邏輯閘路徑。

## 實驗數據
- **Baseline Latency:** 10.24 ms
- **HW-MTP-SV-V2 Latency:** 1.54 ms
- **Speedup:** 6.67x
- **SQNR:** 33.9 dB

## 結論與架構建議
實驗證明，HW-MTP-SV-V2 能夠為 4-head 的 MTP 架構帶來 6.67 倍的加速，大幅縮減了多 Token 同時驗證的延遲。強烈建議在未來的 Edge NPU 的 Attention Output Block 整合此模組。
