# On-Device Learning: QLoRA Bottleneck on Edge Architectures

**Date:** March 30, 2026
**Context:** Prototyping QLoRA (Quantized Low-Rank Adaptation) for true on-device LLM fine-tuning without cloud offloading (Pillar 5).

## 1. The Algorithm
QLoRA allows a user to fine-tune an LLM by freezing the massive base model (stored in compressed 4-bit memory) and only training two tiny, low-rank FP16 matrices ($A$ and $B$). 

## 2. Experimental Results
An initial simulation (`exp_edge_qlora_baseline.py`) tracked the mathematical parameter requirements for a standard $4096 \times 4096$ linear layer with a LoRA rank of $R=8$.

*   **Frozen Weights:** `16,777,216` parameters.
*   **Trainable LoRA Weights:** `65,536` parameters.
*   **Compression:** LoRA successfully reduced the trainable parameter count to **`0.39%`** of the total model. 

## 3. The Bottlenecks (For Auto-Researcher to Improve)

Despite reducing the weights mathematically, QLoRA is currently impossible to run natively on Apple Silicon or Edge mobile devices with long context windows (4K+ tokens) due to a critical memory architectural flaw:

1.  **The Forward Activation Memory Wall:**
    To compute the backward pass (gradients) for the $A$ and $B$ matrices, PyTorch must store the intermediate forward activations ($X$) for every single token in the sequence. For a 4K context window on a 7B model, storing these activations consumes >16GB of VRAM/SRAM. Because Edge NPUs share memory with the CPU, this instantly triggers catastrophic OS SSD swapping, slowing training from minutes to days.
2.  **Gradient Checkpointing is not enough:**
    While we can discard the forward activations and recompute them on-the-fly during the backward pass (Gradient Checkpointing), this trades a memory bottleneck for a compute bottleneck, increasing FLOPs by ~30% and draining battery life rapidly.
3.  **NF4 Dequantization Overhead:**
    The base model weights are stored in 4-bit NormalFloat, but must be dequantized to FP16/BF16 *during* the forward pass matrix multiplication. This requires highly specialized low-level kernels to prevent the dequantization step from becoming memory-bandwidth bound.

## Next Steps for Auto-Researcher
*   **Fix 1:** Explore **Activation-Free Fine-Tuning** methods (e.g., zeroth-order optimization or forward-gradient algorithms) that approximate the gradients for $A$ and $B$ without needing to store the full intermediate computation graph.
*   **Fix 2:** Explore sparse-updating (only updating the LoRA weights on the final 10% of the sequence, ignoring the prefix context) to artificially cap the activation memory requirement.