# AI 加速器自動研究系統 (Auto-Researcher) 每日總結報表
**日期:** 2026-04-13

本報表彙整了 `ai-accelerator-research` 儲存庫中，所有活躍研究支柱 (Research Pillars) 的目前狀態、最新突破與下一步行動。


## 🤖 Auto-Researcher 論文探索總結 (今日最新)

### 📂 分類: NF4_LUT_Quantization
- **論文標題:** TriGen: NPU Architecture for End-to-End Acceleration of Large Language Models based on SW-HW Co-Design
  - **連結:** http://arxiv.org/abs/2602.12962v1
  - **重點:** Recent studies have extensively explored NPU architectures for accelerating AI inference in on-device environments, which are inherently resource-constrained. Meanwhile, transformer-based large langua...

### 📂 分類: NF4_LUT_Quantization
- **論文標題:** PD-Swap: Prefill-Decode Logic Swapping for End-to-End LLM Inference on Edge FPGAs via Dynamic Partial Reconfiguration
  - **連結:** http://arxiv.org/abs/2512.11550v1
  - **重點:** Aggressively quantized large language models (LLMs), such as BitNet-style 1.58-bit Transformers with ternary weights, make it feasible to deploy generative AI on low-power edge FPGAs. However, as prom...

### 📂 分類: NF4_LUT_Quantization
- **論文標題:** T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization
  - **連結:** http://arxiv.org/abs/2511.13676v1
  - **重點:** Recent advances in LLMs have outpaced the computational and memory capacities of edge platforms that primarily employ CPUs, thereby challenging efficient and scalable deployment. While ternary quantiz...

### 📂 分類: NF4_LUT_Quantization
- **論文標題:** Bit-by-Bit: Progressive QAT Strategy with Outlier Channel Splitting for Stable Low-Bit LLMs
  - **連結:** http://arxiv.org/abs/2604.07888v1
  - **重點:** Training LLMs at ultra-low precision remains a formidable challenge. Direct low-bit QAT often suffers from convergence instability and substantial training costs, exacerbated by quantization noise fro...

### 📂 分類: NF4_LUT_Quantization
- **論文標題:** MUXQ: Mixed-to-Uniform Precision MatriX Quantization via Low-Rank Outlier Decomposition
  - **連結:** http://arxiv.org/abs/2604.04701v1
  - **重點:** Large language models (LLMs) have achieved outstanding performance across a wide range of natural language processing tasks, but their enormous parameter counts impose ubstantial memory and computatio...

### 📂 分類: Model_Architecture_CoDesign
- **論文標題:** Cross-Family Speculative Prefill: Training-Free Long-Context Compression with Small Draft Models
  - **連結:** http://arxiv.org/abs/2603.02631v3
  - **重點:** Prompt length is a major bottleneck in agentic large language model (LLM) workloads, where repeated inference steps and multi-call loops incur substantial prefill cost. Recent work on speculative pref...

### 📂 分類: Model_Architecture_CoDesign
- **論文標題:** Align Once, Benefit Multilingually: Enforcing Multilingual Consistency for LLM Safety Alignment
  - **連結:** http://arxiv.org/abs/2602.16660v1
  - **重點:** The widespread deployment of large language models (LLMs) across linguistic communities necessitates reliable multilingual safety alignment. However, recent efforts to extend alignment to other langua...

### 📂 分類: Model_Architecture_CoDesign
- **論文標題:** LatentMoE: Toward Optimal Accuracy per FLOP and Parameter in Mixture of Experts
  - **連結:** http://arxiv.org/abs/2601.18089v1
  - **重點:** Mixture of Experts (MoEs) have become a central component of many state-of-the-art open-source and proprietary large language models. Despite their widespread adoption, it remains unclear how close ex...

### 📂 分類: Model_Architecture_CoDesign
- **論文標題:** Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs
  - **連結:** http://arxiv.org/abs/2510.18245v2
  - **重點:** Scaling the number of parameters and the size of training data has proven to be an effective strategy for improving large language model (LLM) performance. Yet, as these models grow increasingly power...

### 📂 分類: Prefill_Sparse_Prediction
- **論文標題:** PixelPrune: Pixel-Level Adaptive Visual Token Reduction via Predictive Coding
  - **連結:** http://arxiv.org/abs/2604.00886v1
  - **重點:** Document understanding and GUI interaction are among the highest-value applications of Vision-Language Models (VLMs), yet they impose exceptionally heavy computational burden: fine-grained text and sm...

### 📂 分類: Prefill_Sparse_Prediction
- **論文標題:** Beyond Traffic Matrix: DELTA -- A DAG-Aware OCS Logical Topology Optimization for AIDCs
  - **連結:** http://arxiv.org/abs/2603.28096v3
  - **重點:** The rapid scaling of large language models (LLMs) exacerbates communication bottlenecks in AI data centers (AIDCs). To overcome this, optical circuit switches (OCS) are increasingly adopted for their ...

### 📂 分類: Prefill_Sparse_Prediction
- **論文標題:** Prune as You Generate: Online Rollout Pruning for Faster and Better RLVR
  - **連結:** http://arxiv.org/abs/2603.24840v1
  - **重點:** Reinforcement Learning with Verifiable Rewards (RLVR) has significantly advanced the reasoning capabilities of Large Language Models (LLMs). However, methods such as GRPO and DAPO suffer from substant...

### 📂 分類: MoE_Edge_Architecture
- **論文標題:** QaRL: Rollout-Aligned Quantization-Aware RL for Fast and Stable Training under Training--Inference Mismatch
  - **連結:** http://arxiv.org/abs/2604.07853v1
  - **重點:** Large language model (LLM) reinforcement learning (RL) pipelines are often bottlenecked by rollout generation, making end-to-end training slow. Recent work mitigates this by running rollouts with quan...

### 📂 分類: MoE_Edge_Architecture
- **論文標題:** DeepStack: Scalable and Accurate Design Space Exploration for Distributed 3D-Stacked AI Accelerators
  - **連結:** http://arxiv.org/abs/2604.04750v2
  - **重點:** Advances in hybrid bonding and packaging have driven growing interest in 3D DRAM-stacked accelerators with higher memory bandwidth and capacity. As LLMs scale to hundreds of billions or trillions of p...

### 📂 分類: MoE_Edge_Architecture
- **論文標題:** Rethinking Compute Substrates for 3D-Stacked Near-Memory LLM Decoding: Microarchitecture-Scheduling Co-Design
  - **連結:** http://arxiv.org/abs/2604.04253v2
  - **重點:** Large language model (LLM) decoding is a major inference bottleneck because its low arithmetic intensity makes performance highly sensitive to memory bandwidth. 3D-stacked near-memory processing (NMP)...

### 📂 分類: MoE_Edge_Architecture
- **論文標題:** Why Database Manuals Are Not Enough: Efficient and Reliable Configuration Tuning for DBMSs via Code-Driven LLM Agents
  - **連結:** http://arxiv.org/abs/2603.22708v1
  - **重點:** Modern database management systems (DBMSs) expose hundreds of configuration knobs that critically influence performance. Existing automated tuning methods either adopt a data-driven paradigm, which in...

### 📂 分類: MoE_Edge_Architecture
- **論文標題:** AdaFuse: Accelerating Dynamic Adapter Inference via Token-Level Pre-Gating and Fused Kernel Optimization
  - **連結:** http://arxiv.org/abs/2603.11873v1
  - **重點:** The integration of dynamic, sparse structures like Mixture-of-Experts (MoE) with parameter-efficient adapters (e.g., LoRA) is a powerful technique for enhancing Large Language Models (LLMs). However, ...

### 📂 分類: Emerging_Architectures
- **論文標題:** Flux Attention: Context-Aware Hybrid Attention for Efficient LLMs Inference
  - **連結:** http://arxiv.org/abs/2604.07394v1
  - **重點:** The quadratic computational complexity of standard attention mechanisms presents a severe scalability bottleneck for LLMs in long-context scenarios. While hybrid attention mechanisms combining Full At...

### 📂 分類: Emerging_Architectures
- **論文標題:** SISA: A Scale-In Systolic Array for GEMM Acceleration
  - **連結:** http://arxiv.org/abs/2603.29913v1
  - **重點:** The currently dominant AI/ML workloads, such as Large Language Models (LLMs), rely on the efficient execution of General Matrix-Matrix Multiplication (GEMM) operations. Thus, most systems are equipped...

### 📂 分類: Emerging_Architectures
- **論文標題:** SUMMIR: A Hallucination-Aware Framework for Ranking Sports Insights from LLMs
  - **連結:** http://arxiv.org/abs/2604.04947v1
  - **重點:** With the rapid proliferation of online sports journalism, extracting meaningful pre-game and post-game insights from articles is essential for enhancing user engagement and comprehension. In this pape...

### 📂 分類: Emerging_Architectures
- **論文標題:** UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking
  - **連結:** http://arxiv.org/abs/2603.24226v2
  - **重點:** Recent advances in Large Language Models (LLMs) have inspired a surge of scaling law research in industrial search, advertising, and recommendation systems. However, existing approaches focus mainly o...

### 📂 分類: Emerging_Architectures
- **論文標題:** Dynamical Systems Theory Behind a Hierarchical Reasoning Model
  - **連結:** http://arxiv.org/abs/2603.22871v1
  - **重點:** Current large language models (LLMs) primarily rely on linear sequence generation and massive parameter counts, yet they severely struggle with complex algorithmic reasoning. While recent reasoning ar...

### 📂 分類: Emerging_Architectures
- **論文標題:** ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs
  - **連結:** http://arxiv.org/abs/2604.03298v2
  - **重點:** The rapid scaling of Large Language Models presents significant challenges for their deployment and inference, particularly on resource-constrained specialized AI hardware accelerators such as Huawei'...

### 📂 分類: Emerging_Architectures
- **論文標題:** Modernizing Amdahl's Law: How AI Scaling Laws Shape Computer Architecture
  - **連結:** http://arxiv.org/abs/2603.20654v4
  - **重點:** Classical Amdahl's Law conceptualized the limit of speedup for an era of fixed serial-parallel decomposition and homogeneous replication. Modern heterogeneous systems need a different conceptual frame...

### 📂 分類: Emerging_Architectures
- **論文標題:** MINISA: Minimal Instruction Set Architecture for Next-gen Reconfigurable Inference Accelerator
  - **連結:** http://arxiv.org/abs/2603.20623v1
  - **重點:** Modern reconfigurable AI accelerators rely on rich mapping and data-layout flexibility to sustain high utilization across matrix multiplication, convolution, and emerging applications beyond AI. Howev...

### 📂 分類: Emerging_Architectures
- **論文標題:** AutoVeriFix+: High-Correctness RTL Generation via Trace-Aware Causal Fix and Semantic Redundancy Pruning
  - **連結:** http://arxiv.org/abs/2603.11489v1
  - **重點:** Large language models (LLMs) have demonstrated impressive capabilities in generating software code for high-level programming languages such as Python and C++. However, their application to hardware d...


---

## 🧪 AI 自主打樣與驗證報告 (Autonomous Prototyper)
## 🧪 Autonomous Prototype: 2026-04-13
- **Target Bottleneck:** The single most critical unresolved technical bottleneck is the **Forward Activation Memory Wall**, which prevents on-device QLoRA training for 4K+ contexts by consuming excessive SRAM and forcing catastrophic OS SSD swapping on mobile/edge devices.
- **Script Generated:** `auto_prototype_20260413.py`
- **Execution Output / Verdict:**
```text

I0413 07:09:26.137923 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137978 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137981 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137983 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137985 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137989 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137990 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137992 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137994 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137996 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.137999 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.138001 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.138003 9854021 ev_poll_posix.cc:593] FD from fork parent still in poll list: fd(9, generation: 1)
I0413 07:09:26.138005 9854021 
```
---


---

## 🧱 支柱 1: Model Architecture
### 1.1 SSM / Mamba Hybrids (
- **原始碼:** `1_2_ssm_mamba_hybrids`
- **目前狀態:** PyTorch Prototypes Completed.
- **核心發現:** At 4K context, standard $O(N^2)$ GEMM attention outpaces naive $O(N)$ sequential RNN scans on Apple Silicon (MPS). ...
- **瓶頸與下一步:** - **Next Steps:** Lowering the block-parallel logic into actual Apple Metal shaders. ...
### 1.2 Linear Sliding Window (
- **原始碼:** `1_3_linear_sliding_window`
- **目前狀態:** Prototyped and Exported.
- **核心發現:** Implemented an $O(N)$ sliding window attention block tailored for 32K DOM parsing contexts. It efficiently bypasses the massive memory blowup of full ...

## 🧱 支柱 2: Quantization
### 2.1 1.58-Bit Ternary MACs (BitNet) (
- **原始碼:** `2_2_binary_ternary_mac`
- **目前狀態:** Evaluated and Bottleneck Identified.
- **核心發現:** Quantizing weights to `{-1, 0, 1}` removes FP FMA operations, enabling pure Add/Sub matrix multiplications. However, mathematical accuracy dropped to ...
- **瓶頸與下一步:** - **The Bottleneck:** While the integer MAC is fast, scaling factors must be multiplied back in FP16 *after* the integer accumulation. This mixed-prec...
### 2.2 Classical A4A4 Optimizations (
- **原始碼:** `2_3_a4a4_attention_optimizations`
- **目前狀態:** Evaluated and Discarded.
- **核心發現:** - **Methodology:** We established the **Two-Way Validation Principle**: all algorithms must pass both Math SNR (Gate A) and Live LLM Generation (Gate ...
### 2.3 TurboQuant & Sub-4-Bit Architecture (
- **原始碼:** `2_4_turboquant`
- **目前狀態:** Evaluated, Mathematically Formalized, and Verified via Live Qwen 0.5B.
- **核心發現:** A strict ablation study revealed that compressing both Queries and KV cache to 4-bit (A4KV4) causes a 2 dB "Compounding Penalty" ($e_q \cdot e_k$) tha...
- **瓶頸與下一步:** - **The Fix for Attention:** Only **TurboQuant (Orthogonal Rotation) + 1-Bit QJL Residual** survived the A4KV4 Softmax cliff, recovering from a 0% to ...
### 2.4 End-to-End LLM Extreme Quantization: Master Ablation Study (April 2026)
- **原始碼:** `17_1d_hadamard_ablation.py, 19_strict_2d_hadamard_ffn_a4w4.py, 25_a8kv8_a4w4_benchmark.py`
- **目前狀態:** Comprehensive Evaluation Completed on Qwen2.5-0.5B-Instruct.
- **核心發現:** - **Methodology (Fake Quantization & Metrics):** - **W4A4 Block 32 (Sub-Channel Micro-Scaling):** Breakthrough recovery (4.24 dB SNR, 75% Pass Rate). ...
### 2.5 End-to-End A4KV4 & W4A4 Ablation Studies (April 2026 Breakthrough)
- **目前狀態:** Evaluated via PyTorch Monkey-Patching on Qwen2.5-0.5B-Instruct.
### 2.6 Hardware Compensation & QAT Lite (April 2026)
- **目前狀態:** Evaluated and Bottleneck Identified.
- **核心發現:** - **Methodology:** Attempted to rescue the catastrophic A8KV4 + W4A4 configuration by inserting a learnable 1D Affine (Scale & Shift) block before the...
- **瓶頸與下一步:** - **The Bottleneck:** The quantization noise from A4KV4 passed through Softmax is highly non-linear and chaotic. A simple affine transformation cannot...

## 🧱 支柱 3: Dynamic Execution
### 3.1 Token-Level Early-Exit Routing (
- **原始碼:** `3_1_early_exit_routing`
- **目前狀態:** Evaluated and Bottleneck Identified.
- **核心發現:** Simulated forcing 80% of "easy" tokens to skip the last 8 layers of a 16-layer transformer, achieving a theoretical FLOPs/Latency reduction of `~38%`....
- **瓶頸與下一步:** - **The Bottleneck:** The PyTorch gather/scatter operations (boolean masking) needed to route tokens introduce severe memory bandwidth overhead. Readi...
### 3.2 Early-Exit Classifiers (
- **原始碼:** `3_2_early_exit_classifiers`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Modeled the computational overhead of running a confidence scorer (e.g., an MLP) at every layer boundary. ...
- **瓶頸與下一步:** - **The Bottleneck:** The latency spent calculating "should I exit?" often exceeds the latency saved by actually exiting. Needs zero-classifier heuris...
### 3.3 Flexible N:M Structured Sparsity (
- **原始碼:** `3_3_flexible_nm_sparsity`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Simulated a 2:4 structured sparse weight matrix by masking 50% of elements to zero. ...
- **瓶頸與下一步:** - **The Bottleneck:** Without specialized tensor cores (like Nvidia Ampere), Apple Silicon and generic Edge NPUs still execute the floating-point math...
### 3.4 Token Pruning (
- **原始碼:** `3_1_token_pruning`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Physically dropping 50% of the least-attended tokens halves the sequence length for deeper layers. ...
- **瓶頸與下一步:** - **The Bottleneck:** Changing the sequence length dynamically destroys static batching and padding on NPUs (like the Apple Neural Engine), forcing sl...
### 3.5 MoE Drafter Speculative Decoding Bandwidth Simulation (April 2026)
- **目前狀態:** Cycle-Accurate Memory Simulation Completed.
- **核心發現:** - **Methodology:** Simulated a 68M parameter MoE Drafter (17M active per token, W4A4 Block 32) on a mobile LPDDR5x interface (50 GB/s) with a 32MB SLC...

## 🧱 支柱 4: Memory-Centric (KV Cache & Attention)
### 4.1 Tableless Hash Embeddings (
- **原始碼:** `4_2_tableless_hash_embeds`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Replaced a 131MB embedding table (`32000x4096`) with a 16MB hashed table (`4096x4096`), achieving an 8x memory reduction. ...
- **瓶頸與下一步:** - **The Bottleneck:** Deterministic hashing creates exact collisions. Multiple unique vocabulary tokens map to the identical vector, destroying semant...

## 🧱 支柱 5: On-Device Learning
### 5.1 Edge QLoRA Architecture (
- **原始碼:** `5_1_edge_qlora`
- **目前狀態:** Evaluated and Bottleneck Identified.
- **核心發現:** QLoRA successfully compresses trainable parameters to `< 0.4%` of the base LLM. However, it cannot be run on mobile/edge devices for 4K+ contexts. ...
- **瓶頸與下一步:** - **The Bottleneck:** The Forward Activation Memory Wall. PyTorch must store the full intermediate activation tensor $X$ for every token in the 4K seq...
### 5.2 Hardware LoRA Updates (
- **原始碼:** `5_1_hardware_lora_updates`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Modeled the physical memory matrix operations for computing the $dA$ gradient. ...
- **瓶頸與下一步:** - **The Bottleneck:** Transposing the massive $X$ (Activations) matrix for $X^T \cdot dY \cdot B^T$ completely destroys CPU/GPU cache locality. Needs ...
### 5.3 Gradient Compression (
- **原始碼:** `5_2_gradient_compression`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Simulated compressing backprop gradients down to 8-bit. ...
- **瓶頸與下一步:** - **The Bottleneck:** The presence of a single gradient outlier destroys the dynamic range of the 8-bit scale, causing the MSE error to explode and di...

## 🧱 支柱 6: Diffusion Transformers (DiT)
### 6.1 Step Distillation & LCM (
- **原始碼:** `6_1_step_distillation_lcm`
- **目前狀態:** Baseline Prototyped.
- **核心發現:** Simulated a 50-step ODE Diffusion solver vs a 4-step Latent Consistency Model (LCM). Proved a `>90%` latency reduction. ...
- **瓶頸與下一步:** - **The Bottleneck:** LCM enforces smooth trajectories, inherently destroying high-frequency noise sampling and causing outputs to appear blurry and l...

