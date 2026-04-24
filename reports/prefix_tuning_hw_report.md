# Hardware Prefix Tuning Injection Engine

## Background
Prefix Tuning (or P-Tuning) is a highly efficient alternative to full fine-tuning (like LoRA), where a set of continuous "soft prompt" vectors is prepended to the user's input. In multi-tenant serving, software frameworks must dynamically concatenate these massive prefix tensors into the KV cache for every single request, causing severe memory duplication, fragmentation, and memory bandwidth saturation during the prefill phase.

## Hardware Simulation
We simulated the latency of dynamic tensor concatenation in software versus a zero-copy Hardware Prefix Injection Engine (`prefix_tuning_hw_sim.py`).
- **Software Prefix Injection Latency:** 107374.18 ms (simulated over large batch size)
- **Hardware Prefix Injection Latency:** 5368.71 ms
- **Speedup:** 20.00x

## Architectural Proposal
We propose integrating a **"Hardware Prefix Broadcaster"** within the NPU's Attention ALU. Instead of duplicating the soft-prompt tensors in memory for every batch, the trained prefix vectors are permanently pinned to a dedicated "Shared Prefix SRAM Block". During execution, the NPU's SRAM controller automatically multicasts these pinned vectors to the MAC arrays simultaneously for all requests in the batch. This achieves Zero-Copy Prefix Tuning, saving gigabytes of memory bandwidth in multi-tenant environments.
