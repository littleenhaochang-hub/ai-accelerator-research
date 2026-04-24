# Attention Zero-Skipping Hardware Engine

## Background
In long-context LLMs, the Softmax attention matrix becomes extremely sparse, with the vast majority of tokens yielding near-zero attention scores towards irrelevant historical context. Computing full-precision $Q \cdot K^T$ for these tokens wastes immense amounts of MAC energy and SRAM bandwidth. 

## Hardware Simulation
We simulated the latency of standard dense attention versus an "Attention Zero-Skipping" hardware block (`attention_zero_skipping_sim.py`). The skipping block uses a lightweight ultra-low-precision predictor (using only $d/16$ channels) to estimate attention magnitude, discarding 85% of the $O(N^2)$ computations before they reach the main Tensor Core.
- **Dense Attention Latency:** 8.5899 s (for 8K sequence, per head)
- **Zero-Skipped Attention Latency:** 1.8254 s
- **Speedup:** 4.71x

## Architectural Proposal
We propose integrating a **"Hardware Attention Pre-Predictor & Zero-Skipping Engine"** directly into the Attention ALU of Edge NPUs. By quickly evaluating a heavily subsampled query-key pair, this engine dynamically gates the primary MAC arrays, forcing them into a sleep state for low-relevance tokens. This delivers a nearly 5x speedup in long-context prefill operations without the overhead of complex block-sparse indexing.
