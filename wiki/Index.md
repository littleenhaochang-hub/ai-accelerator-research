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
