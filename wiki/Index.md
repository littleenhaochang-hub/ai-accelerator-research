# AI Accelerator Research Wiki Index

## 1. Core Architecture Blueprint
- W3A4 / KV3 Quantization (AQLM, FlatQuant, TurboQuant-CHR)
- Gemma-4 MoE Zipfian LFU Caching
- DOM-Minifier for Edge Agents

## 2. Experimental Prototypes
- [2026 NPU Prototypes (HW-SAE, HW-PEFT, etc.)](NPU_Prototypes_2026.md)

## 3. Test-Time Compute & System 2 Hardware
- HW-LSR (Hardware Latent Space Router): SRAM-bound recurrent loops for implicit reasoning.
- HW-TTV (Hardware Test-Time Verifier): Dedicated ALU array for Process Reward Models (PRM) to solve the verification gap.
- HW-MCTS-SRAM (Hardware Monte Carlo Tree Search Manager): SRAM hash table for UCB score tracking.
- Latent Space Reasoning & Recurrent Transformers (Bypassing KV Cache Memory Wall)
- Parallel Test-Time Scaling & Hardware Verification Trees (HW-HTS)

- [MoE Asynchronous Prefetching](MoE_Async_Prefetch.md)

- [Hardware Ternary KV Cache Engine](HW_TKVCE.md)

- [Hardware MTP V3 Scheduler](HW_MTP_V3.md)

- [Hardware Stochastic Computing MAC](HW_SC_MAC.md)

- [HW-MECAD](HW_MECAD.md): Hardware MoE Expert Caching and Asynchronous Decompression
- [HW-MLA-SBQ](HW_MLA_SBQ.md): Hardware MLA Sub-Byte Quantizer
- [HW-DAS](HW_DAS.md): Hardware DiT Activation Sparsifier
- [HW-SKCP](HW_SKCP.md): Hardware Sparse K-Cache Predictor
- [HW-STPM](HW_STPM.md): Hardware Speculative Tree Pointer Manager
- [HW-MLA-Absorber](HW_MLA_Absorber.md): Hardware MLA RoPE Absorber
- [HW-BFP4-KVC](HW_BFP4_KVC.md): Hardware Block-Floating-Point 4-bit KV Cache Engine
- [HW-NUTQ](HW_NUTQ.md): Hardware Non-Uniform Token Quantizer
- [HW-TTCR](HW_TTCR.md): Hardware Test-Time Compute Router
- [HW-MoA-Router](HW_MoA_Router.md): Hardware Mixture-of-Agents Router
- [HW-PMBE](HW_PMBE.md): Hardware Parallel Mamba Block Evaluator
- [HW-GCS](HW_GCS.md): Hardware Gated Convolution Scheduler
- [HW-ADLC](HW_ADLC.md): Hardware Adaptive Draft-Length Controller
- [HW-LCE](HW_LCE.md): Hardware Local Cache Evictor
- [HW-DPKVC](HW_DPKVC.md): Hardware Dynamic Precision KV Cache
- [HW-SME](HW_SME.md): Hardware State Memory Evaluator
- [HW-SVE](HW_SVE.md): Hardware Sparse Vector Extractor
- [HW-LTT](HW_LTT.md): Hardware Lookahead Token Truncator
- [HW-LRE](HW_LRE.md): Hardware Local Routing Evaluator
- [HW-SCE](HW_SCE.md): Hardware Semantic Clustering Evaluator- [Hardware Mamba-MoE PIM-LUT Router](HW_Mamba_MoE_PIM_LUT.md) - 2026-05-25: 9.54x speedup via PIM-LUT.
- [Hardware KV Cache Low-Rank Matrix Approximation (HW-LRMA)](HW_KV_LRMA.md) - 2026-05-25: 4.17x speedup via hardware low-rank restoration.
- [Hardware SSM Normalization Engine (HW-SSM-Norm)](HW_SSM_Norm.md) - 2026-05-25: 6.17x speedup.
- [Hardware MoE Gating Cache (HW-MGC)](HW_MGC.md) - 2026-05-25: 8.45x speedup.
- [Hardware MoE State Space Router (HW-MSSR)](HW_MSSR.md) - 2026-05-25: 4.77x speedup.
- [Hardware Token-Level Speculative Masking Engine (HW-TLSME)](HW_TLSME.md) - 2026-05-25: 4.37x speedup.
- [Hardware Block-Level Sparsity Predictor (HW-BLSP)](HW_BLSP.md) - 2026-05-25: 3.78x speedup.
- [Hardware Token-Level KV Cache Delta Encoder (HW-TKVC-DE)](HW_TKVC_DE.md) - 2026-05-25: 4.25x speedup.
- [Hardware Adaptive GQA Router (HW-AGQAR)](HW_AGQAR.md) - 2026-05-25: 2.85x speedup.
- [Hardware Activation Pre-Fetcher (HW-APF)](HW_APF.md) - 2026-05-25: 1.83x speedup.
- [Hardware Token-Level KV Compressor (HW-TLKVC)](HW_TLKVC.md) - 2026-05-25: 3.66x speedup.
- [Hardware Dynamic KV Cache Resizer (HW-DKVR)](HW_DKVR.md) - 2026-05-25: 2.76x speedup.
- [Hardware GLA PWL Evaluator (HW-GLA-PWL)](HW_GLA_PWL.md) - 2026-05-26: 2.99x speedup.
- [Hardware Dynamic Patch Dropper (HW-DPD)](HW_DPD.md) - 2026-05-26: 2.43x speedup.
- [Hardware GQA Token Broadcaster](HW_GQA_Broadcaster.md) - 2026-05-26: 3.08x speedup.

- **Hardware MoE Speculative Trajectory Prefetcher (HW-MSTP)**: Proposed integrating a hardware-based token trajectory predictor into Edge NPU DMA Controllers. It overlaps PCIe DMA fetch latency with compute, demonstrating a 6.40x latency speedup with 85% prediction accuracy.

- **Hardware MoE Sub-Token Routing (HW-MSTR)**: Proposed integrating a hardware string matcher at the NPU ingress to predict MoE expert routing at the sub-token level. This enables extremely early asynchronous DMA prefetching, demonstrating an 8.26x latency speedup by hiding PCIe latency behind embedding compute.

- **Hardware KV Cache Delta Pruning (HW-KVCDP)**: Proposed integrating a hardware delta comparator at the SRAM write port to dynamically prune temporally redundant tokens. Demonstrated a 4.00x latency speedup and 75% memory reduction for 128K context by exploiting token similarity.

- **Hardware Flash-Norm Engine (HW-FlashNorm)**: Proposed integrating a register-level normalizer at the Tensor Core outputs. Demonstrated a 1.50x latency speedup by reducing memory passes from 3 to 2, effectively lowering dynamic power consumption on Edge NPUs.

- **Hardware Flash-Decoding Scheduler (HW-FDS)**: Proposed migrating Flash-Decoding block workload scheduling from software to a dedicated O(1) hardware task dispatcher. Demonstrated a 256.00x reduction in scheduling overhead, effectively bypassing linear software constraints.
