# Linear Attention Hardware Simulation Report
## 背景 (Background)
O(N) Linear Attention (如 Katharopoulos 等人提出的特徵映射方法) 透過改變矩陣乘法順序，將傳統 O(N^2) 的注意力機制降低至 O(N)，解決長文本 Memory Bound 瓶頸。

## 模擬參數 (Parameters)
- Sequence Length: 16384
- Head Dimension: 64

## 模擬結果 (Results)
- 傳統 O(N^2) 延遲: 1717.99 µs
- Linear O(N) 延遲: 6.71 µs
- 運算加速比: 256.00x

## 架構建議 (Architectural Proposal)
為了高效支援 Linear Attention，Edge NPU 需針對 **$D 	imes D$ 維度的小矩陣乘法**進行最佳化。有別於傳統 $N 	imes D$ 大規模乘法，Linear Attention 會頻繁對 Head Dimension 進行累加 (KV Accumulation)。建議硬體新增一個緊鄰 SRAM 的 **KV State Accumulator Array**，專門處理這類小維度連續更新。
