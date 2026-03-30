# Architecture Exploration Proposal

## 1. Next-Gen Attention (`1_1_next_gen_attention`)
**Current State:** Advanced. We have successfully prototyped "Low-Rank Factorization for Up-Projection Matrices" and a "Fused Low-Rank MLA Up-Projection Kernel."
**Prototyping Plan:** Deploy the fused kernel to Apple Silicon (MPS) for empirical profiling. We must verify if the memory bandwidth savings hold true under Edge constraints before moving to quantization integration.

## 2. SSM / Mamba Hybrids (`1_2_ssm_mamba_hybrids`)
**Current State:** Unexplored (empty directory).
**Prototyping Plan:** Draft initial PyTorch prototypes comparing Mamba associative scans versus standard FlashAttention GEMMs. The goal is to evaluate if SSM hardware hybrids can eliminate the $O(N^2)$ prefill bottleneck for context lengths > 32K without degrading generation accuracy.

## 3. Linear Attention / Sliding Window (`1_3_linear_sliding_window`)
**Current State:** Unexplored (empty directory).
**Prototyping Plan:** Implement $O(N)$ Linear Attention and sliding window algorithms specifically tailored for DOM Minifier/Truncator workflows. This is critical for scaling edge agentic AI, as current 32K web page context pushes prefill latency to ~2 minutes. We will build a test suite to measure Input TPS vs window size.

---
**Execution:** I will begin scaffolding the PyTorch kernels for the SSM and Sliding Window prototypes immediately.