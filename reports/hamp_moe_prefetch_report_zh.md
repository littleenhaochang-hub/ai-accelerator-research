# Hardware Asynchronous MoE Prefetching (HAMP) 實驗報告

## 摘要
在處理 MoE (Mixture of Experts) 架構時，傳統的 CPU-GPU 記憶體傳輸 (PCIe bandwidth bottleneck) 是主要的效能瓶頸。本實驗旨在驗證「硬體非同步 MoE 預取 DMA (HAMP)」架構，透過在背景預取專家權重以重疊傳輸與運算時間。

## 實驗設定
- 專家模型大小: 128 MB
- PCIe 頻寬: 32 GB/s
- 每個 token 運算時間: 1 ms
- 測試 token 數量: 1000

## 實驗結果
- **傳統循序載入延遲 (Baseline):** 4.9062 秒
- **HAMP 非同步預取延遲:** 3.9072 秒
- **效能提升 (Speedup):** 1.26x

## 結論與硬體架構建議
實驗證明，透過將 PCIe 傳輸與矩陣運算 (MAC) 重疊，可有效降低 MoE 解碼的延遲。我們強烈建議在下一代 Edge NPU 的 DMA 控制器中整合「HAMP 預取引擎」，以徹底發揮硬體管線的吞吐量。
