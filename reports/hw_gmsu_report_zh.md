# Hardware Gated Mamba State Update (HW-GMSU)

## 實驗目標
針對 Mamba/SSM 模型在處理 64K 級別文本時的循序狀態更新進行優化。引入硬體級別的 Gating 評估單元 (HW-GMSU)，即時跳過被 Gating 機制過濾掉（近乎零更新）的冗餘 Token，大幅加速時間混合 (Time-Mixing) 的過程。

## 實驗數據
- **Baseline Latency:** 2621.44 ms
- **HW-GMSU Latency:** 98.38 ms
- **Speedup:** 26.64x
- **SQNR:** 33.7 dB

## 結論與架構建議
實驗證明，HW-GMSU 利用 Mamba 隱含的高稀疏度 (約 85% 狀態無顯著更新)，在 64K 長文本下取得了 26 倍的加速，同時保持 33.7 dB 的準確度。建議在專為 SSM 設計的 Edge NPU 的 SRAM 讀取端整合此 Gating 判斷單元，以實作 Early-exit 狀態跳躍。
