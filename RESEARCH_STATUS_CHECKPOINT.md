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
- **Architectural Decision:** Dense rotation (TurboQuant) combined with a 1-Bit QJL residual is the officially verified, superior path for Edge AI A4A4 quantization.

---

## Pillar 3: Dynamic Execution

### 3.1 Token-Level Early-Exit Routing (`3_1_early_exit_routing`)
- **Status:** Evaluated and Bottleneck Identified.
- **Findings:** Simulated forcing 80% of "easy" tokens to skip the last 8 layers of a 16-layer transformer, achieving a theoretical FLOPs/Latency reduction of `~38%`.
- **The Bottleneck:** The PyTorch gather/scatter operations (boolean masking) needed to route tokens introduce severe memory bandwidth overhead. Reading sparse token indices from memory is often slower than just computing the dense matrix multiplication on GPUs/NPUs. 

---

## Pillar 4: Memory-Centric (KV Cache & Attention)

### 4.3 TurboQuant & A4 Fusion (`4_3_kv_cache_turboquant`)
- **Status:** Evaluated and Resolved the "Softmax Cliff".
- **Findings:** Fusing 4-bit activations (A4) with 4-bit rotated KV Cache (TurboQuant) causes quantization variance to compound ($e_q \cdot e_k$). The Softmax function exponentially amplifies this noise, destroying the Signal-to-Noise Ratio (SNR) and causing a 0% pass rate in live text generation.
- **The Fix (1-Bit QJL):** We implemented a 1-bit residual correction (+1/-1 sign of the compression error). Adding this to the hardware MAC via Popcount recovers +4.18 dB of SNR.
- **Live Validation:** Monkey-patched a live `Qwen2.5-0.5B-Instruct` model. While standard A4A4 collapsed into silence or gibberish, the 5-bit QJL pipeline successfully recovered semantic English generation (40-60% task pass rate).

---

## Pillar 5: On-Device Learning

### 5.1 Edge QLoRA Architecture (`5_1_edge_qlora`)
- **Status:** Evaluated and Bottleneck Identified.
- **Findings:** QLoRA successfully compresses trainable parameters to `< 0.4%` of the base LLM. However, it cannot be run on mobile/edge devices for 4K+ contexts.
- **The Bottleneck:** The Forward Activation Memory Wall. PyTorch must store the full intermediate activation tensor $X$ for every token in the 4K sequence to compute gradients for the $A$ and $B$ LoRA matrices. This consumes >16GB of SRAM, forcing catastrophic OS SSD swapping.

---

## Global Next Steps for Auto-Researcher
1. **Pillar 2.2 (Ternary):** Design an algorithm that absorbs FP16 scale factors into the activation function (SiLU/GeLU) so the accumulator doesn't stall.
2. **Pillar 3.1 (Routing):** Explore "Zero-Out" dense routing (setting the token vector to exactly 0.0) to short-circuit the ALU without breaking dense memory contiguous blocks.
3. **Pillar 5.1 (Edge Training):** Explore Activation-Free Fine-Tuning methods (e.g., zeroth-order optimization or forward-gradient algorithms) to train LoRA without storing the full intermediate computation graph.
4. **Pillar 1.2 (SSM):** Lowering the block-parallel Mamba logic into actual Apple Metal shaders.