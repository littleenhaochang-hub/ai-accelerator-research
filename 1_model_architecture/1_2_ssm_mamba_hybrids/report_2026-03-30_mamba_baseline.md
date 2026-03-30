# SSM Mamba Hybrids vs Standard GEMM Attention

## Experiment: Naive RNN vs GEMM

**Objective:** Benchmark the baseline execution time of a sequential $O(N)$ state-space model scan versus highly optimized $O(N^2)$ GEMM standard attention operations to highlight why custom hardware/kernels are necessary for Edge SSM deployment.

**Results (Context: 4,096 tokens, d_model: 256):**
- Mamba (Naive RNN Scan): `0.0348s`
- Standard Attention (GEMM): `0.0272s`

**Analysis:** 
At 4K context length, standard $O(N^2)$ attention still beats the naive $O(N)$ sequential RNN loop because matrix multiplication (GEMMs) is highly optimized in PyTorch/MPS. 

**Conclusion:** 
To actually realize the theoretical scaling benefits of Mamba for context lengths > 32K on Apple Silicon (Edge), we must implement a parallel associative scan using custom Metal/Triton kernels rather than standard sequential loops. This will form the next stage of our SSM hardware-software co-design prototyping.