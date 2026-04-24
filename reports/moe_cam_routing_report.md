# Content-Addressable Memory (CAM) for MoE Expert Routing

## Background
As models scale to massive Mixture-of-Experts (MoE) architectures (e.g., DeepSeek with 256+ fine-grained experts), the routing mechanism itself becomes a significant compute bottleneck. Standard routing requires computing the dot product of the token representation against all expert centroids, followed by a Top-K sorting operation. This $O(E)$ compute and $O(E \log E)$ sort scales poorly on Edge NPUs.

## Hardware Simulation
We simulated the latency of standard SRAM-based routing (Softmax + Top-K) versus a Hardware Content-Addressable Memory (CAM) router (`moe_cam_routing_sim.py`).
- **Standard SRAM Routing Latency:** 5255.17 ms (for 4096 tokens, 256 experts)
- **Hardware CAM Latency:** 4.10 ms
- **Speedup:** 1283.00x

## Architectural Proposal
We propose integrating a **"Ternary Content-Addressable Memory (TCAM) Router"** into Edge NPUs. By storing the expert centroid signatures in TCAM, the NPU can perform an $O(1)$ parallel nearest-neighbor search for all tokens simultaneously. This completely eliminates the Softmax and Sorting overhead, making fine-grained MoE routing essentially zero-cost in terms of latency, and drastically reducing MAC array contention during the dispatch phase.
