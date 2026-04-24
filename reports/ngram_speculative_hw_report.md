# Hardware N-Gram Speculative Decoding Engine

## Background
Speculative Decoding traditionally requires a separate, smaller "draft model" to predict future tokens, which are then verified by the main model. On Edge NPUs, running a draft model still incurs significant memory bandwidth overhead and competes for the same MAC arrays. Research suggests that for many generative tasks (e.g., code generation, agentic DOM navigation), simple N-gram statistics can predict tokens with surprisingly high acceptance rates.

## Hardware Simulation
We simulated the token generation latency of using a standard 1B parameter draft model versus a dedicated SRAM-based N-Gram Cache Lookup Engine (`ngram_speculative_hw_sim.py`).
- **Draft Model Speculative Latency:** 30.72 ms
- **SRAM N-Gram Speculative Latency:** 2.05 ms
- **Speedup:** 15.00x

## Architectural Proposal
We propose integrating a **"Hardware N-Gram Cache Tracker"** into the NPU. During the prefill and decode phases, this dedicated SRAM block autonomously builds an N-gram transition table of the current context. During generation, it instantaneously provides zero-cost token drafts directly to the main model for verification, entirely eliminating the need for a secondary neural network and bypassing the MAC array bottleneck.
