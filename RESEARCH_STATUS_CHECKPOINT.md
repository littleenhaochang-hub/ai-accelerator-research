# AI Accelerator Research - Status Checkpoint
**Date:** March 30, 2026

This document serves as the master state-tracker for the AI Accelerator Research repository. It summarizes all experimental findings, architectural decisions, and current prototype statuses across the active research pillars.

---

## Pillar 1: Model Architecture

### 1.2 SSM / Mamba Hybrids (`1_2_ssm_mamba_hybrids`)
- **Status:** PyTorch Prototypes Completed.
- **Findings:** At 4K context, standard $O(N^2)$ GEMM attention outpaces naive $O(N)$ sequential RNN scans on Apple Silicon (MPS). 
- **Solution:** Developed `block_parallel_scan.py` to simulate a hardware-aware chunked parallel scan. It successfully breaks the $O(N)$ sequential dependency, mimicking $O(\log N)$ Triton/Metal thread-block execution.
- **Next Steps:** Lowering the block-parallel logic into actual Apple Metal shaders.

### 1.3 Linear Sliding Window (`1_3_linear_sliding_window`)
- **Status:** Prototyped and Exported.
- **Findings:** Implemented an $O(N)$ sliding window attention block tailored for 32K DOM parsing contexts. It efficiently bypasses the massive memory blowup of full $O(N^2)$ attention.
- **Deployment:** Successfully traced and compiled the PyTorch graph into a pure `sliding_window.tflite` model using the Google `litert-torch` toolchain. Ready for edge deployment profiling.

---

## Pillar 2: Quantization

### 2.2 1.58-Bit Ternary MACs (BitNet) (`2_2_binary_ternary_mac`)
- **Status:** Evaluated and Bottleneck Identified.
- **Findings:** Quantizing weights to `{-1, 0, 1}` removes FP FMA operations, enabling pure Add/Sub matrix multiplications. However, mathematical accuracy dropped to `~5.8 dB` SNR when applied as Post-Training Quantization (PTQ) to standard LLM weights. 
- **The Bottleneck:** While the integer MAC is fast, scaling factors must be multiplied back in FP16 *after* the integer accumulation. This mixed-precision barrier creates pipeline stalls on rigid NPUs (like the Apple Neural Engine).

### 2.3 Classical A4A4 Optimizations (`2_3_a4a4_attention_optimizations`)
- **Status:** Evaluated and Discarded.
- **Methodology:** We established the **Two-Way Validation Principle**: all algorithms must pass both Math SNR (Gate A) and Live LLM Generation (Gate B).
- **Findings:** Tested Percentile Clipping, Block/Group Quant (G=32), and Sparse-Dense Hybrids against the Qwen 0.5B model.
- **Verdict:** While the Sparse-Dense hybrid scored an incredible 41.23 dB in raw mathematical SNR, it catastrophically failed the live text generation test (broken grammar/hallucinations). Extracting outliers into sparse matrices breaks the model's structural timing (e.g., RoPE).
- **Architectural Decision:** Dense rotation (TurboQuant) combined with a 1-Bit QJL residual is the officially verified, superior path for Edge AI A4KV4 Attention.

### 2.4 TurboQuant & Sub-4-Bit Architecture (`2_4_turboquant` & `2_5_attention_ablation`)
- **Status:** Evaluated, Mathematically Formalized, and Verified via Live Qwen 0.5B.
- **Findings:** A strict ablation study revealed that compressing both Queries and KV cache to 4-bit (A4KV4) causes a 2 dB "Compounding Penalty" ($e_q \cdot e_k$) that triggers the Softmax Cliff, completely destroying generative coherence.
- **The Fix for Attention:** Only **TurboQuant (Orthogonal Rotation) + 1-Bit QJL Residual** survived the A4KV4 Softmax cliff, recovering from a 0% to 40-60% task pass rate by smearing outliers and applying popcount residual fixes. Sub-channel quantization failed due to Softmax scaling errors.
- **The Fix for FFNs:** In FFN layers (post-SiLU), TurboQuant struggles due to asymmetric structural outliers. However, **Sub-Channel E8M0** perfectly isolates FFN outliers (achieving 18.35 dB SNR) while eliminating floating-point multipliers (Multiplier-Free) with zero memory-bandwidth tax.
- **Architectural Decision:** Edge NPUs must use TurboQuant+QJL for Attention, and Sub-Channel E8M0 for FFNs.

---

## Pillar 3: Dynamic Execution

### 3.1 Token-Level Early-Exit Routing (`3_1_early_exit_routing`)
- **Status:** Evaluated and Bottleneck Identified.
- **Findings:** Simulated forcing 80% of "easy" tokens to skip the last 8 layers of a 16-layer transformer, achieving a theoretical FLOPs/Latency reduction of `~38%`.
- **The Bottleneck:** The PyTorch gather/scatter operations (boolean masking) needed to route tokens introduce severe memory bandwidth overhead. Reading sparse token indices from memory is often slower than just computing the dense matrix multiplication on GPUs/NPUs. 

### 3.2 Early-Exit Classifiers (`3_2_early_exit_classifiers`)
- **Status:** Baseline Prototyped.
- **Findings:** Modeled the computational overhead of running a confidence scorer (e.g., an MLP) at every layer boundary.
- **The Bottleneck:** The latency spent calculating "should I exit?" often exceeds the latency saved by actually exiting. Needs zero-classifier heuristics (e.g., cosine similarity tracking).

### 3.3 Flexible N:M Structured Sparsity (`3_3_flexible_nm_sparsity`)
- **Status:** Baseline Prototyped.
- **Findings:** Simulated a 2:4 structured sparse weight matrix by masking 50% of elements to zero.
- **The Bottleneck:** Without specialized tensor cores (like Nvidia Ampere), Apple Silicon and generic Edge NPUs still execute the floating-point math for the zeroes. Zero-masking provides 0% speedup. Needs software-level vector packing.

### 3.2 Token Pruning (`3_1_token_pruning`)
- **Status:** Baseline Prototyped.
- **Findings:** Physically dropping 50% of the least-attended tokens halves the sequence length for deeper layers.
- **The Bottleneck:** Changing the sequence length dynamically destroys static batching and padding on NPUs (like the Apple Neural Engine), forcing slow dynamic graph re-compilations. Needs a "Zero-Masking" approach instead.

---

## Pillar 4: Memory-Centric (KV Cache & Attention)

### 4.2 Tableless Hash Embeddings (`4_2_tableless_hash_embeds`)
- **Status:** Baseline Prototyped.
- **Findings:** Replaced a 131MB embedding table (`32000x4096`) with a 16MB hashed table (`4096x4096`), achieving an 8x memory reduction.
- **The Bottleneck:** Deterministic hashing creates exact collisions. Multiple unique vocabulary tokens map to the identical vector, destroying semantic precision for rare words. Needs a Multi-Hashing concatenation strategy.

---

## Pillar 5: On-Device Learning

### 5.1 Edge QLoRA Architecture (`5_1_edge_qlora`)
- **Status:** Evaluated and Bottleneck Identified.
- **Findings:** QLoRA successfully compresses trainable parameters to `< 0.4%` of the base LLM. However, it cannot be run on mobile/edge devices for 4K+ contexts.
- **The Bottleneck:** The Forward Activation Memory Wall. PyTorch must store the full intermediate activation tensor $X$ for every token in the 4K sequence to compute gradients for the $A$ and $B$ LoRA matrices. This consumes >16GB of SRAM, forcing catastrophic OS SSD swapping.

### 5.2 Hardware LoRA Updates (`5_1_hardware_lora_updates`)
- **Status:** Baseline Prototyped.
- **Findings:** Modeled the physical memory matrix operations for computing the $dA$ gradient.
- **The Bottleneck:** Transposing the massive $X$ (Activations) matrix for $X^T \cdot dY \cdot B^T$ completely destroys CPU/GPU cache locality. Needs a Transpose-Free Backprop algorithm.

### 5.3 Gradient Compression (`5_2_gradient_compression`)
- **Status:** Baseline Prototyped.
- **Findings:** Simulated compressing backprop gradients down to 8-bit.
- **The Bottleneck:** The presence of a single gradient outlier destroys the dynamic range of the 8-bit scale, causing the MSE error to explode and diverging QLoRA fine-tuning. Needs Block-Floating Point (BFP) or Error-Feedback.

---

## Pillar 6: Diffusion Transformers (DiT)

### 6.1 Step Distillation & LCM (`6_1_step_distillation_lcm`)
- **Status:** Baseline Prototyped.
- **Findings:** Simulated a 50-step ODE Diffusion solver vs a 4-step Latent Consistency Model (LCM). Proved a `>90%` latency reduction.
- **The Bottleneck:** LCM enforces smooth trajectories, inherently destroying high-frequency noise sampling and causing outputs to appear blurry and lack micro-details. Needs a phased DDIM-injection strategy.

---

## Global Next Steps for Auto-Researcher
1. **Pillar 7 (Next-Gen Paradigms):** Build initial baselines for Test-Time Compute (DeepSeek-R1 style branching), RetNet (decay matrix vs GEMM on Apple Silicon), and Mixture-of-Depths (sparse-dense token routing).
2. **Pillar 2.2 (Ternary):** Design an algorithm that absorbs FP16 scale factors into the activation function (SiLU/GeLU) so the accumulator doesn't stall.
3. **Pillar 3.1 (Routing):** Explore "Zero-Out" dense routing (setting the token vector to exactly 0.0) to short-circuit the ALU without breaking dense memory contiguous blocks.
4. **Pillar 5.1 (Edge Training):** Explore Activation-Free Fine-Tuning methods (e.g., zeroth-order optimization or forward-gradient algorithms) to train LoRA without storing the full intermediate computation graph.
5. **Pillar 1.2 (SSM):** Lowering the block-parallel Mamba logic into actual Apple Metal shaders.