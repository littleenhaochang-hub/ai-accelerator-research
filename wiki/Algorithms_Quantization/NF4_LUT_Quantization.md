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


## 🤖 Auto-Researcher Update: 2026-04-12
### TriGen: NPU Architecture for End-to-End Acceleration of Large Language Models based on SW-HW Co-Design
- **發表時間:** 2026-02-13T14:28:31Z
- **論文連結:** http://arxiv.org/abs/2602.12962v1
- **摘要:** Recent studies have extensively explored NPU architectures for accelerating AI inference in on-device environments, which are inherently resource-constrained. Meanwhile, transformer-based large language models (LLMs) have become dominant, with rapidly increasing model sizes but low degree of parameter reuse compared to conventional CNNs, making end-to-end execution on resource-limited devices extremely challenging. To address these challenges, we propose TriGen, a novel NPU architecture tailored for resource-constrained environments through software-hardware co-design. Firstly, TriGen adopts low-precision computation using microscaling (MX) to enable additional optimization opportunities while preserving accuracy, and resolves the issues that arise by employing such precision. Secondly, to jointly optimize both nonlinear and linear operations, TriGen eliminates the need for specialized hardware for essential nonlinear operations by using fast and accurate LUT, thereby maximizing performance gains and reducing hardware-cost in on-device environments, and finally, by taking practical hardware constraints into account, further employs scheduling techniques to maximize computational utilization even under limited on-chip memory capacity. We evaluate the performance of TriGen on various LLMs and show that TriGen achieves an average 2.73x performance speedup and 52% less memory transfer over the baseline NPU design with negligible accuracy loss.


## 🤖 Auto-Researcher Update: 2026-04-12
### PD-Swap: Prefill-Decode Logic Swapping for End-to-End LLM Inference on Edge FPGAs via Dynamic Partial Reconfiguration
- **發表時間:** 2025-12-12T13:35:09Z
- **論文連結:** http://arxiv.org/abs/2512.11550v1
- **摘要:** Aggressively quantized large language models (LLMs), such as BitNet-style 1.58-bit Transformers with ternary weights, make it feasible to deploy generative AI on low-power edge FPGAs. However, as prompts grow to tens of thousands of tokens, edge hardware performance drops sharply with sequence length due to quadratic prefill cost and rapidly increasing KV-cache bandwidth demands, making inference latency of longer context length a first-order system concern. Recent studies on LLMs expose a fundamental prefill-decode asymmetry: prefill is compute-bound and dominated by dense matrix-matrix operations, whereas decoding is memory-bandwidth-bound and dominated by KV-cache traffic. A static accelerator must provision resources and a single dataflow for both regimes, leading to duplicated attention logic, underutilized fabric, and tight LUT/URAM limits that cap model size and usable context. We propose a prefill--decode disaggregated LLM accelerator, PD-Swap, that uses Dynamic Partial Reconfiguration (DPR) to time-multiplex the attention module on edge FPGAs. The core table-lookup ternary matrix multiplication and weight-buffering engines remain static, while the attention subsystem is a reconfigurable partition with two phase-specialized architectures: a compute-heavy, token-parallel prefill engine and a bandwidth-optimized, KV-cache-centric decoding engine. A roofline-inspired model and design space exploration jointly optimize reconfigurable-region size, parallelism under reconfiguration and routability constraints, and reconfiguration latency is hidden by computation latency. PD-Swap achieves up to 27~tokens/s decoding throughput, outperforming prior state-of-the-art works by 1.3x--2.1x (larger gains at longer context lengths), without extra area cost.


## 🤖 Auto-Researcher Update: 2026-04-12
### T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization
- **發表時間:** 2025-11-17T18:32:03Z
- **論文連結:** http://arxiv.org/abs/2511.13676v1
- **摘要:** Recent advances in LLMs have outpaced the computational and memory capacities of edge platforms that primarily employ CPUs, thereby challenging efficient and scalable deployment. While ternary quantization enables significant resource savings, existing CPU solutions rely heavily on memory-based lookup tables (LUTs) which limit scalability, and FPGA or GPU accelerators remain impractical for edge use. This paper presents T-SAR, the first framework to achieve scalable ternary LLM inference on CPUs by repurposing the SIMD register file for dynamic, in-register LUT generation with minimal hardware modifications. T-SAR eliminates memory bottlenecks and maximizes data-level parallelism, delivering 5.6-24.5x and 1.1-86.2x improvements in GEMM latency and GEMV throughput, respectively, with only 3.2% power and 1.4% area overheads in SIMD units. T-SAR achieves up to 2.5-4.9x the energy efficiency of an NVIDIA Jetson AGX Orin, establishing a practical approach for efficient LLM inference on edge platforms.

