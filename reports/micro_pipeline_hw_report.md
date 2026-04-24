# Hardware Micro-Pipeline Parallelism for Token Generation

## Background
During autoregressive decoding (generation phase), standard software frameworks execute token operations layer-by-layer. Even in continuous batching, a token must wait for its entire batch to complete layer $L$ before moving to layer $L+1$. This introduces massive pipeline bubbles and drastically increases Time-Between-Tokens (TBT), severely degrading the user experience for real-time Agentic workflows.

## Hardware Simulation
We simulated the token generation latency of standard layer-by-layer execution versus a Hardware Micro-Pipeline (`micro_pipeline_hw_sim.py`). In the micro-pipeline, tokens flow through the hardware layers individually without batch synchronization boundaries.
- **Standard Layer-by-Layer Latency:** 325.00 ms (for 1000 tokens across 32 layers, simulated scale)
- **Hardware Micro-Pipeline Latency:** 10.32 ms
- **Speedup:** 31.49x

## Architectural Proposal
We propose replacing standard NPU batch schedulers with an **"Asynchronous Token Micro-Pipeline Controller"**. Rather than synchronizing at layer boundaries, this hardware controller passes individual token state vectors directly from the output registers of Layer $L$ to the input queue of Layer $L+1$. By decoupling token execution from batch synchronization, Edge NPUs can achieve theoretically perfect compute-bound latency during the decoding phase.
