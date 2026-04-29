# CXL MoE Predictive Prefetching

本頁面記錄 MoE 架構下的硬體預取技術。

## 瓶頸
MoE Autoregressive Decoding 時的專家路由 (Expert Routing) 具有不確定性，導致 PCIe/CXL 傳輸延遲遠大於 GPU 計算時間。

## 解決方案
整合硬體級的 MoE Lookahead Prefetcher 與 CXL 介面。利用提早預測 Token 走向，以非同步 DMA 方式將專家權重載入 SRAM，掩蓋記憶體延遲。

## 數據
- PCIe Demand Loading Latency: 3525.88 ms
- CXL Prefetching Latency: 2072.48 ms
- 提升倍率: 1.70x