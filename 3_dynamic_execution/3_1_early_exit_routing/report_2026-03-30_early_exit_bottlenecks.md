# Dynamic Token Routing: Early-Exit Latency vs Overhead Analysis

**Date:** March 30, 2026
**Context:** Experimenting with dynamic execution (Pillar 3) to skip unnecessary computation layers for "easy" tokens (e.g., punctuation, articles) to save battery and latency on Edge devices.

## 1. The Algorithm
Instead of passing all tokens through all $N$ layers of the Transformer, an internal "confidence scorer" evaluates if a token's representation is stable (e.g., early-exit at layer 8 out of 16). 
Tokens that exit early save massive amounts of FLOPs in the remaining FFN and Attention layers.

## 2. Experimental Results
An initial simulation (`exp_early_exit_routing.py`) forced 80% of tokens to "early-exit" at Layer 8 out of a 16-layer stack. 

*   **Standard Dense (All Layers):** `0.182s`
*   **Early-Exit Sparse Routing:** `0.112s`
*   **Latency Reduction:** `~38%`

## 3. The Bottlenecks (For Auto-Researcher to Improve)

This approach poses three severe challenges that the next wave of research must solve:

1.  **The Gather/Scatter Memory Tax:**
    To skip computation for specific tokens, you must physically gather the remaining active tokens into a contiguous block, compute on them, and scatter them back into the main sequence. These `boolean masking` and `index selection` memory operations are extremely hostile to GPU caches and Edge NPUs. The memory bandwidth overhead of gathering often cancels out the FLOPs saved by not computing the easy tokens.
2.  **KV Cache Consistency Breakdown:**
    If a token "exits" at layer 8, it doesn't compute Key/Value representations for layers 9-16. But what happens if a token at layer 15 needs to "attend" to that exited token? The Key doesn't exist. The baseline prototype ignores this, but a real LLM would crash or hallucinate.
3.  **Confidence Calibrator Overhead:**
    To know *when* a token should exit, you have to compute a softmax confidence score at every layer boundary. The cost of running the classifier itself eats into the latency savings.

## Next Steps for Auto-Researcher
*   **Fix 1:** Design an architecture where the KV cache is "shared" or projected forward across layers, so exited tokens still provide Keys/Values to the deeper layers without needing to run their own FFNs.
*   **Fix 2:** Instead of gathering/scattering tokens (sparse memory), explore "Zero-Out" dense routing (setting the token vector to exactly 0.0), allowing the hardware to quickly short-circuit the multiplication at the ALU level without breaking the dense memory contiguous blocks.