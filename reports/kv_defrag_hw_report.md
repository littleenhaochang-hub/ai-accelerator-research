# Hardware Background KV Cache Defragmenter

## Background
In continuous batching environments, the SRAM physical memory allocating PagedAttention KV blocks becomes highly fragmented over time as requests finish and free non-contiguous pages. To maintain contiguous bursts for maximum bandwidth, memory defragmentation is occasionally required. Doing this in software halts the NPU decoding pipeline, causing severe latency spikes (tail latency) for real-time Agentic users.

## Hardware Simulation
We simulated the token stall latency caused by software-based memory compaction versus a dedicated Hardware Background Defragmentation Engine (`kv_defrag_hw_sim.py`).
- **Software Defrag Stall Latency:** 512.00 ms (for 1GB of fragmentation)
- **Hardware Defrag Stall Latency:** 10.24 ms
- **Speedup:** 50.00x

## Architectural Proposal
We propose integrating a **"Hardware Background Defragmenter"** into the NPU Memory Controller. This unit leverages an asynchronous DMA engine to transparently move KV cache pages and update the physical page tables while the main Tensor Cores are busy executing MAC operations. By hiding memory compaction behind compute, the NPU eliminates 500ms+ garbage collection stalls, ensuring perfectly smooth continuous token generation.
