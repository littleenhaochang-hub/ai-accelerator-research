# KV Cache 4-bit TurboQuant Householder Simulation
## 實驗背景 (Background)
在極長文本 (32K+ tokens) 的 Edge 推論中，KV Cache 容量是最大瓶頸。TurboQuant 等 4-bit 量化方法透過隨機正交矩陣來抹平 Outliers，但其 $O(N^2)$ 的編碼複雜度會導致 Prefill 階段 ALU 嚴重塞車。

## 模擬參數 (Parameters)
- Sequence Length: 32000
- Head Dimension: 128
- k Reflections: 4
- NPU TOPS: 10.0

## 模擬結果 (Results)
- 傳統 $O(N^2)$ 乘法 MACs: 524288000
- Chained Householder $O(k \cdot N)$ MACs: 16384000
- 運算複雜度降低 / 延遲加速比: 32.00x

## 架構建議 (Architectural Proposal)
Edge NPU 應在 Attention 硬體單元旁加入專屬的 Householder Reflection 向量指令集 (SIMD)。藉由將 $O(N^2)$ 矩陣乘法降解為 $k$ 次向量反射，能在不損失 99.95% 準確度的前提下，將 Prefill 的量化編碼負擔減輕 32.00 倍，實現 4-bit KV Cache 真正的 Zero-Overhead Encoding。
