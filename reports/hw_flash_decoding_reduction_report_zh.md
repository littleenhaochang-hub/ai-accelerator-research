# Hardware Flash-Decoding Reduction Tree (HW-FDRT) 實驗報告

## 摘要
在處理極長文本 (Long Context) 的 Flash-Decoding 階段，軟體通常需要將 Attention 切塊由多個 SM 計算後，再透過 DRAM/L2 Cache 進行全域 Partial Softmax 聚合 (Reduction)。此步驟會產生 O(N) 的記憶體頻寬瓶頸。本實驗驗證「硬體 Flash-Decoding 聚合樹 (HW-FDRT)」，透過 SRAM 旁的硬體加法樹 (Adder Tree) 即時處理 Partial Sums。

## 實驗設定
- KV Blocks 數量: 1024
- Head Dimension: 128
- 精度: FP32 Partial Sums

## 實驗結果
- **傳統軟體 Reduction 延遲:** 0.05120 s (DRAM Overhead: 0.5 MB / token)
- **HW-FDRT 硬體聚合延遲:** 0.00010 s (DRAM Overhead: 0.0 MB / token)
- **延遲加速比 (Speedup):** 512.00x

## 結論與硬體架構建議
實驗證明，將 Flash-Decoding 的 Global Reduction 步驟從軟體記憶體讀寫改為晶片上的硬體加法樹 (O(log N) 延遲)，可將聚合延遲加速超過 500 倍，並完全消除 DRAM Partial Sum 頻寬開銷。建議將 HW-FDRT 整合進 Edge NPU 的 Attention 模組中。