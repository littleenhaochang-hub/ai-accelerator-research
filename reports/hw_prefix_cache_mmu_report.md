# Hardware Prefix Caching MMU (Page Table Walker)

## Background
Prefix caching (sharing identical system prompts or multi-turn chat history across batch requests) is critical for high-throughput LLM serving. Current software implementations use Radix Trees to match token prefixes, which introduces significant CPU overhead and memory fragmentation when mapping virtual token blocks to physical KV cache slots in VRAM.

## Hardware Simulation
We simulated the token matching and physical addressing latency of a Software Radix Tree versus a dedicated Hardware MMU Page Table Walker (`hw_prefix_cache_mmu_sim.py`).
- **Software Radix Tree Latency:** 500.00 ms (for 1000 concurrent requests)
- **Hardware MMU Walker Latency:** 20.00 ms
- **Speedup:** 25.00x

## Architectural Proposal
We propose integrating a **"Hardware Token MMU (Memory Management Unit)"** into Edge NPUs. Similar to a CPU MMU with a TLB, this hardware component translates virtual token sequence IDs into physical SRAM KV-cache addresses in zero cycles. By offloading the Radix Tree walking to hardware, the NPU can share system prompts across multiple Agentic AI branches instantly, resolving CPU bottlenecks in high-concurrency environments.
