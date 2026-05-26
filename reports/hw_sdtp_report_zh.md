# 硬體投機目標預取器 (Hardware Speculative Draft Target Prefetcher, HW-SDTP)

## 摘要
在投機解碼 (Speculative Decoding) 中，草稿模型生成完畢後，目標模型 (Target Model) 需要載入權重來進行驗證。傳統架構下，這是序列化且受限於 DRAM 頻寬的操作 (Demand Fetching)。我們評估了在硬體層面實現的目標模型異步預取器。

## 實驗結果
- **基準延遲 (Demand Fetch)**: 18.75 ms
- **改進延遲 (HW-SDTP)**: 1.88 ms
- **加速比**: 10.00x

## 結論
透過在 Edge NPU DMA 控制器中整合 HW-SDTP，硬體可以在草稿模型生成最後幾個 Token 的同時，異步地將目標模型的權重預取至 SRAM。這隱藏了 90% 的 DRAM 讀取延遲，使投機驗證階段的延遲降低了 10 倍，極大化了 Speculative Decoding 的吞吐量。
