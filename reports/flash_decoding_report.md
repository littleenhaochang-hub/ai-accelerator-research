# FlashDecoding 硬體加速架構分析

## 實驗背景
在 LLM 生成階段 (Decoding Phase)，對於極長文本 (例如 32K tokens)，傳統 Attention 需要掃描歷史中所有的 KV 向量才能產生單一 Token 的輸出。由於 Batch Size=1，矩陣乘法退化為矩陣-向量乘法 (GEMV)，導致嚴重的記憶體頻寬瓶頸，且無法充分利用現代 NPU 的平行運算資源。為了解決這個問題，我們針對 FlashDecoding 演算法進行硬體層級的模擬。

## 實驗方法
撰寫 `flash_decoding_sim.py`，模擬 32K context 且 Batch Size 為 1 的 Decoding 階段。
FlashDecoding 的核心是將 KV 序列切成多個 Blocks (例如 Block Size = 256)，並分配給不同的 Compute Units (模擬 32 個) 平行處理，各自算出局部的 Attention 輸出與 Max 值，最後再進行全域的 Softmax Reduction。

## 實驗數據
- **Context Length**: 32K tokens
- **Baseline Decoding Latency**: 2684.35 us
- **FlashDecoding Latency**: 83.93 us
- **Effective Throughput Speedup**: 31.98x

## 硬體架構結論
透過將 KV 讀取並行化，FlashDecoding 在長文本下能帶來高達將近 32 倍的生成加速。
從硬體架構的角度來看，要將其效益最大化，邊緣 NPU 需要在多個 Compute Units 之間整合專屬的 **Global Reduction Network (全域歸約網路)**。這樣能將各單元 SRAM 算出的 Partial Softmax Sums 直接在硬體層級進行快速匯整 (Aggregation)，避免再次透過 DRAM 進行讀寫，徹底消除 Reduction 階段的瓶頸。
