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

## 🤖 Auto-Researcher Update: 2026-04-13
### QaRL: Rollout-Aligned Quantization-Aware RL for Fast and Stable Training under Training--Inference Mismatch
- **發表時間:** 2026-04-09T06:11:46Z
- **論文連結:** http://arxiv.org/abs/2604.07853v1
- **摘要:** Large language model (LLM) reinforcement learning (RL) pipelines are often bottlenecked by rollout generation, making end-to-end training slow. Recent work mitigates this by running rollouts with quantization to accelerate decoding, which is the most expensive stage of the RL loop. However, these setups destabilize optimization by amplifying the training-inference gap: rollouts are operated at low precision, while learning updates are computed at full precision. To address this challenge, we propose QaRL (Rollout Alignment Quantization-Aware RL), which aligns training-side forward with the quantized rollout to minimize mismatch. We further identify a failure mode in quantized rollouts: long-form responses tend to produce repetitive, garbled tokens (error tokens). To mitigate these problems, we introduce TBPO (Trust-Band Policy Optimization), a sequence-level objective with dual clipping for negative samples, aimed at keeping updates within the trust region. On Qwen3-30B-A3B MoE for math problems, QaRL outperforms quantized-rollout training by +5.5 while improving stability and preserving low-bit throughput benefits.


## 🤖 Auto-Researcher Update: 2026-04-13
### DeepStack: Scalable and Accurate Design Space Exploration for Distributed 3D-Stacked AI Accelerators
- **發表時間:** 2026-04-06T15:16:35Z
- **論文連結:** http://arxiv.org/abs/2604.04750v2
- **摘要:** Advances in hybrid bonding and packaging have driven growing interest in 3D DRAM-stacked accelerators with higher memory bandwidth and capacity. As LLMs scale to hundreds of billions or trillions of parameters, distributed inference across multiple 3D chips becomes essential. With cross-stack co-design increasingly critical, we propose DeepStack, an accurate and efficient performance model and tool to enable early-stage system-hardware co-design space exploration (DSE) for distributed 3D-stacked AI systems. At the hardware level, DeepStack captures fine-grained 3D memory semantics such as transaction-aware bandwidth, bank activation constraints, buffering limitations, and thermal-power modeling. At the system level, DeepStack incorporates comprehensive parallelization strategies and execution scheduling for distributed LLM inference. With novel modeling techniques such as dual-stage network abstraction and tile-level compute-communication overlap, we achieve up to 100,000x faster runtime over state-of-the-art simulators at comparable accuracy, cross-validated against our in-house 3D designs, NS-3 backend (2.12%), and vLLM serving on 8xB200 GPUs (12.18%). With hierarchical design space search, DeepStack enables efficient exploration over 2.5x10^14 design points spanning 3D-stacked DRAM layers, DRAM vertical connectivity, interconnect, compute-memory allocation, and distributed scheduling. Compared with baseline designs, DeepStack achieves up to 9.5x higher throughput through co-optimized parallelism and 3D architecture search. Our DSE further reveals that batch size drives a more fundamental architectural divide than the prefill/decode distinction, and that parallelism strategy and hardware architecture are tightly coupled -- incomplete schedule search leads to permanently suboptimal silicon irrecoverable by software tuning. We intend to open source DeepStack to support future research.


## 🤖 Auto-Researcher Update: 2026-04-13
### Rethinking Compute Substrates for 3D-Stacked Near-Memory LLM Decoding: Microarchitecture-Scheduling Co-Design
- **發表時間:** 2026-04-05T20:18:54Z
- **論文連結:** http://arxiv.org/abs/2604.04253v2
- **摘要:** Large language model (LLM) decoding is a major inference bottleneck because its low arithmetic intensity makes performance highly sensitive to memory bandwidth. 3D-stacked near-memory processing (NMP) provides substantially higher local memory bandwidth than conventional off-chip interfaces, making it a promising substrate for decode acceleration. However, our analysis shows that this bandwidth advantage also shifts many decode operators on 3D-stacked NMP back into the compute-bound regime. Under the tight area budget of the logic die, the design of the compute substrate itself therefore becomes a first-order challenge. Therefore, we rethink the compute microarchitecture of prior 3D-stacked NMP designs. First, we replace prior MAC tree-based compute units with a more area-efficient systolic array, and we further observe that decode operators exhibit substantial shape diversity, making reconfigurability in both systolic array shape and dataflow essential for sustaining high utilization. Building on this insight, we continue to exploit two key opportunities: the high local memory bandwidth reduces the need for large on-chip buffers, and the existing vector core, originally designed to handle auxiliary tensor computations, already provides much of the control logic and multi-ported buffering required for fine-grained flexibility for systolic array, allowing us to unify the two structures in a highly area-efficient manner. Based on these insights, we present the first compute microarchitecture tailored to 3D-stacked NMP LLM decoding, explicitly designed to satisfy the joint requirements of low area cost, high-bandwidth operation, and fine-grained reconfigurability. We further propose an multi-core scheduling framework. Compared with Stratum, our design achieves an average 2.91x speedup and 2.40x higher energy efficiency across both dense and MoE models.


## 🤖 Auto-Researcher Update: 2026-04-13
### Why Database Manuals Are Not Enough: Efficient and Reliable Configuration Tuning for DBMSs via Code-Driven LLM Agents
- **發表時間:** 2026-03-24T02:00:34Z
- **論文連結:** http://arxiv.org/abs/2603.22708v1
- **摘要:** Modern database management systems (DBMSs) expose hundreds of configuration knobs that critically influence performance. Existing automated tuning methods either adopt a data-driven paradigm, which incurs substantial overhead, or rely on manual-driven heuristics extracted from database documentation, which are often limited and overly generic. Motivated by the fact that the control logic of configuration knobs is inherently encoded in the DBMS source code, we argue that promising tuning strategies can be mined directly from the code, uncovering fine-grained insights grounded in system internals. To this end, we propose SysInsight, a code-driven database tuning system that automatically extracts fine-grained tuning knowledge from DBMS source code to accelerate and stabilize the tuning process. SysInsight combines static code analysis with LLM-based reasoning to identify knob-controlled execution paths and extract semantic tuning insights. These insights are then transformed into quantitative and verifiable tuning rules via association rule mining grounded in tuning observations. During online tuning, system diagnosis is applied to identify critical knobs, which are adjusted under the rule guidance. Evaluations demonstrate that compared to the SOTA baseline, SysInsight converges to the best configuration on average 7.11X faster while achieving a 19.9% performance improvement.


## 🤖 Auto-Researcher Update: 2026-04-13
### AdaFuse: Accelerating Dynamic Adapter Inference via Token-Level Pre-Gating and Fused Kernel Optimization
- **發表時間:** 2026-03-12T12:46:42Z
- **論文連結:** http://arxiv.org/abs/2603.11873v1
- **摘要:** The integration of dynamic, sparse structures like Mixture-of-Experts (MoE) with parameter-efficient adapters (e.g., LoRA) is a powerful technique for enhancing Large Language Models (LLMs). However, this architectural enhancement comes at a steep cost: despite minimal increases in computational load, the inference latency often skyrockets, leading to decoding speeds slowing by over 2.5 times. Through a fine-grained performance analysis, we pinpoint the primary bottleneck not in the computation itself, but in the severe overhead from fragmented, sequential CUDA kernel launches required for conventional dynamic routing. To address this challenge, we introduce AdaFuse, a framework built on a tight co-design between the algorithm and the underlying hardware system to enable efficient dynamic adapter execution. Departing from conventional layer-wise or block-wise routing, AdaFuse employs a token-level pre-gating strategy, which makes a single, global routing decision for all adapter layers before a token is processed. This "decide-once, apply-everywhere" approach effectively staticizes the execution path for each token, creating an opportunity for holistic optimization. We capitalize on this by developing a custom CUDA kernel that performs a fused switching operation, merging the parameters of all selected LoRA adapters into the backbone model in a single, efficient pass. Experimental results on popular open-source LLMs show that AdaFuse achieves accuracy on par with state-of-the-art dynamic adapters while drastically cutting decoding latency by a factor of over 2.4x, thereby bridging the gap between model capability and inference efficiency.

