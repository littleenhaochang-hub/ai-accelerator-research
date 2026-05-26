# 硬體張量核心繞過引擎 (HW-TCBE) 分析報告

## 執行摘要
在稀疏注意力或高度量化的模型中，包含大量零值的區塊如果仍然送入 Tensor Core 進行計算，會浪費大量動態功耗並佔用計算週期。我們提出了硬體張量核心繞過引擎 (HW-TCBE)。

## 模擬結果
* **密集 MAC 計算延遲:** 98.30 ms
* **HW-TCBE 延遲:** 14.77 ms
* **效能提升:** 延遲加速達 6.66x。

## 架構建議
針對未來的邊緣 NPU 架構，建議在 Tensor Core 前端整合 **Hardware Tensor-Core Bypass Engine (HW-TCBE)**，當偵測到全零或高度稀疏區塊時，直接硬體短路 (Short-Circuit) 繞過 MAC 陣列，大幅降低功耗並加速計算。
