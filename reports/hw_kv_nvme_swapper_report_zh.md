# 硬體 NVMe KV Cache 交換器 (Hardware NVMe KV Swapper) 模擬報告

## 執行摘要
測試使用硬體 P2P DMA 直接從 NVMe 載入/卸載 KV Cache，繞過作業系統的 Page Fault 機制。

## 實驗結果
- **加速比:** 8.00x
- **建議:** 於 NPU 中整合硬體 NVMe KV Cache P2P 交換控制器。