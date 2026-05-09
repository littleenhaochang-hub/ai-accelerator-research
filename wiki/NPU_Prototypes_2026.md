# 2026 Edge NPU Hardware-Software Co-Design Prototypes

## 1. HW-SAE (Hardware Spiking Attention Engine)
- **Status:** Evaluated (7.38x Speedup)
- **Mechanism:** Bypasses MAC units for low-activation tokens using thresholding. Uses Condition-Addition instead of multiplication for sparse attention logic.

## 2. HW-PEFT (Hardware Parameter-Efficient Context Switching)
- **Status:** Evaluated (7.20x Speedup)
- **Mechanism:** Zero-delay LoRA SRAM switching. Allocates a dedicated scratchpad for Agent weights, swapping context by updating a pointer without DRAM I/O.

## 3. HW-HACB (Hierarchical Attention Cache Buffer)
- **Mechanism:** Asynchronous DMA prefetching for KV Cache. Preloads tokens N+1 to N+4 into L1 Cache while N is computing.

## 4. HW-HFATP (Hardware-Fused Activation Token Pruning)
- **Mechanism:** Real-time entropy calculation on the data bus for Vision-Language Patches. Drops low-entropy (background) tokens before matrix multiplication.

## 5. HW-HTS (Hardware Tree Search for Speculative Decoding)
- **Mechanism:** ASIC logic gate specifically for validating Draft Model token trees in 1 clock cycle, eliminating CPU-NPU communication latency.
