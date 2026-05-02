# 硬體動態 Token 壓縮引擎 (Hardware Dynamic Token Compressor) 模擬報告

## 執行摘要
測試硬體層級的動態 Token 壓縮機制，以減少在 Transformer 各層間傳遞的多餘背景 Token 運算。

## 實驗結果
- **加速比:** 9.74x
- **建議:** 於 NPU 中整合硬體動態 Token 壓縮單元。