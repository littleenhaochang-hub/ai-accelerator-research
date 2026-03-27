# Auto-Research Report: AI Accelerators & LLM Optimizations
**Date:** March 27, 2026
**Target:** arXiv (cs.AR, cs.LG, cs.AI) & Top Conferences (ICLR, ICML, ISCA, MICRO, HPCA, ISSCC)

## Top 3 New Papers

### 1. AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization
**Summary:** This paper introduces an LLM-driven agentic system that autonomously optimizes compute kernels for AI accelerators (tested specifically on AWS Trainium). It iteratively writes, compiles, tests, and refines kernel code to improve throughput and cost-effectiveness.
**Analysis (Is it a good idea?):** Yes, it is highly practical. Kernel optimization is currently a massive bottleneck that requires scarce ninja-level hardware engineers. Automating this with a self-improving agent loop directly addresses the compute utilization problem on non-NVIDIA hardware (like Trainium or custom ASICs).
**Prototype Plan:**
- **Goal:** Build a mini-AccelOpt for Triton on NVIDIA/AMD GPUs.
- **Steps:**
  1. Set up an evaluation harness measuring GEMM/FlashAttention kernel execution time using OpenAI's Triton.
  2. Prompt an LLM (e.g., Claude 3.5 Sonnet or GPT-4o) with a baseline Triton kernel and performance profile.
  3. Create an automated loop where the LLM proposes loop-unrolling, block-size tuning, or memory access adjustments, compiles it, runs the benchmark, and uses the error/latency feedback to iteratively improve the kernel.

### 2. MAHL: Multi-Agent LLM-Guided Hierarchical Chiplet Design with Adaptive Debugging
**Summary:** Proposes using a multi-agent LLM framework to guide the hierarchical design of chiplets for AI accelerators. The agents collaborate on floorplanning, routing, and power estimation, applying adaptive debugging when constraints (PPA - Power, Performance, Area) are violated.
**Analysis (Is it a good idea?):** Conceptually strong, but practically risky. EDA (Electronic Design Automation) tools are notoriously rigid and require formal verification. Relying on LLMs for layout/routing might lead to hallucinatory designs that fail DRC (Design Rule Checks). However, for high-level architectural exploration and chiplet partitioning, it's a brilliant way to search the vast design space quickly.
**Prototype Plan:**
- **Goal:** Simulate chiplet partitioning and bandwidth estimation using an LLM swarm.
- **Steps:**
  1. Define a workload graph (e.g., a Transformer block).
  2. Implement two LLM agents: "Architect" (proposes chiplet boundaries and memory placement) and "Evaluator" (calculates cross-chiplet communication overhead and latency using a simple analytical model).
  3. Run an iterative negotiation loop between them to minimize off-chiplet bandwidth while respecting compute-per-chiplet limits.

### 3. DS-LLM: Leveraging Dynamical Systems to Enhance Both Training and Inference of Large Language Models (ICLR 2025)
**Summary:** This ICLR 2025 paper models the forward pass of LLMs as a discrete-time dynamical system. By applying principles from dynamical systems theory, it skips redundant computations and layers during both training and inference, drastically reducing energy consumption without accuracy degradation.
**Analysis (Is it a good idea?):** Excellent. Viewing residual networks and transformers as dynamical systems/ODEs is theoretically grounded (similar to Neural ODEs). Applying this to dynamically skip layers or halt computation early based on the state trajectory is a highly scalable optimization, perfectly suited for real-time edge AI or cost-sensitive cloud serving.
**Prototype Plan:**
- **Goal:** Implement early-exit (layer skipping) in a small open-source LLM using dynamical state stabilization metrics.
- **Steps:**
  1. Load a small LLM (e.g., Llama-3-8B) in PyTorch/HuggingFace.
  2. Inject a monitor between transformer blocks that calculates the cosine similarity or L2 distance of the hidden states between consecutive layers.
  3. If the state change drops below a threshold $\epsilon$ (indicating the "dynamical system" has reached a fixed point), halt computation and pass the state directly to the language modeling head.
  4. Benchmark token latency and perplexity trade-offs on a local dataset.

