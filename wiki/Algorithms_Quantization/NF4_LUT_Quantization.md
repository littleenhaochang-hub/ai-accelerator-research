# NF4 LUT Quantization vs Linear Bit-Shifting

## The Problem with Linear A4W4
Using linear subchannel scaling (e.g., `e8m0` power-of-2 shifts) for 4-bit weights destroys FFN blocks due to massive outliers (SwiGLU). Qwen2.5 ablation showed linear A4W4 drops PPL to an unacceptable 18.17.

## The LUT Solution
Instead of forcing weights into 16 equidistant linear buckets, we map them to a **NormalFloat4 (NF4) Look-Up Table** that aligns with the normal distribution curve (dense in the middle, sparse at the tails).

## Hardware Efficiency
*   **Area Cost:** Effectively zero. A 16-element FP16 lookup table fits in a tiny SRAM register shared globally.
*   **Bandwidth:** Maintains the exact same 4-bit memory footprint as linear scaling.
*   **Quality Recovery:** Recovers WikiText-2 PPL from 18.17 down to 10.34, halving the mathematical noise (SQNR +4dB).

*Related: [[Hardware_Architecture/FP24_Accumulator]]*

## 🤖 Auto-Researcher Update: 2026-04-11
### LEXI: Lossless Exponent Coding for Efficient Inter-Chiplet Communication in Hybrid LLMs
- **Published:** 2026-03-16T17:48:30Z
- **Link:** http://arxiv.org/abs/2603.15589v1
- **Summary:** Data movement overheads increase the inference latency of state-of-the-art large language models (LLMs). These models commonly use the bfloat16 (BF16) format for stable training. Floating-point standards allocate eight bits to the exponent, but our profiling reveals that exponent streams exhibit fewer than 3 bits Shannon entropy, indicating high inherent compressibility. To exploit this potential, we propose LEXI, a novel lossless exponent compression scheme based on Huffman coding. LEXI compresses activations and caches on the fly while storing compressed weights for just-in-time decompression near compute, without sacrificing system throughput and model accuracy. The codecs at the ingress and egress ports of network-on-chip routers sustain the maximum link bandwidth via multi-lane LUT decoders, incurring only 0.09 percent area and energy overheads with GF 22 nm technology. LEXI reduces inter-chiplet communication and end-to-end inference latencies by 33-45 percent and 30-35 percent on modern Jamba, Zamba, and Qwen LLMs implemented on a homogeneous chiplet architecture.


## 🤖 Auto-Researcher Update: 2026-04-11
### FAST-Prefill: FPGA Accelerated Sparse Attention for Long Context LLM Prefill
- **Published:** 2026-02-24T03:36:25Z
- **Link:** http://arxiv.org/abs/2602.20515v1
- **Summary:** In long-context large language model (LLM) inference, the prefill stage dominates computation due to self-attention over the complete input context. Sparse attention significantly reduces self-attention computation by limiting each token's interactions to a subset of tokens. The attention sparsity pattern varies across input prompts, and within a prompt, each attention head can follow a distinct pattern. This makes attention sparsity dynamic. The requirement of generating the sparsity pattern, combined with limited data reuse in attention, shifts the prefill compute to being memory-bound. This, in addition to the huge energy requirements for long-context inference on GPU, motivates FPGAs as good candidates for accelerating dynamic long-context inference.   To tackle these challenges, we propose FAST-Prefill, the first FPGA accelerator for long-context prefill-stage inference with dynamic sparse attention. To efficiently generate sparse indices, we propose a \textit{fused pipeline unit with a memory-aware execution order} to reduce large tensors and irregular memory accesses. To reduce off-chip memory traffic for accessing the KV cache, we utilize the memory hierarchy to design a \textit{liveness-driven, dual-tier cache}. For high-throughput matrix multiplication, we design a \textit{hybrid Matrix Processing Unit (MPU)} with DSPs and bit-plane decomposition using LUTs. We implement FAST-Prefill on Alveo U280 and evaluate it on the Llama and Qwen models (batch size = 1) for context lengths ranging from 4K to 128K tokens. We demonstrate an average speedup of up to 2.5$\times$ in TTFT and 4.5$\times$ improvement in energy efficiency over GPU implementation on Nvidia A5000 GPU.

