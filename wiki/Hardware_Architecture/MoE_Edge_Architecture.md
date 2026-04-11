# MoE Edge Architecture (Gemma-4 26B)

## Physical Constraints
Running a 26B MoE model natively on a 16GB Apple Silicon device is impossible due to memory limits.
*   **Total W4A4 Footprint:** ~12.6GB Flash + 1.2GB Pinned DRAM (Shared Experts & Embeddings).

## Zipfian LFU Caching Strategy
Through time-over-space layer-wise routing profiles (150k tokens), we discovered extreme Zipfian long-tail skew in expert activation.
*   **Cache Allocation:** 3.8GB dynamic DRAM cache.
*   **Strategy:** Least Frequently Used (LFU). We cache the 42 most statistically active experts (out of 128) per layer.
*   **Hit Rate:** 87.3% during autoregressive decoding.

## I/O Latency Masking
For the 12.7% cache misses, we use SG-DMA (Scatter-Gather) pre-fetching. The router determines token assignments before the FFN block executes, allowing asynchronous UFS 4.0 reads to mask latency behind the Attention block's compute cycles.

*Related: [[NF4_LUT_Quantization]]*
