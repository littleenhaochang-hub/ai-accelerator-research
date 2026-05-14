# Deep Research: Test-Time Compute & System 2 Reasoning Framework

## 1. Core Paradigm Shift
This report synthesizes the latest literature on shifting intelligence from pre-training scale (parameter count) to inference-time search (Test-Time Compute). By enabling SLMs to explicitly or implicitly explore multiple reasoning paths, we can match the performance of LLMs >10x their size.

## 2. Key Algorithmic Breakthroughs
- We study a novel language model architecture that is capable of scaling test-time computation by implicitly reasoning in latent space. Our model works by iterating a recurrent block, thereby unrolling to arbitrary depth at test-time. This stands in contrast to mainstream reasoning models that scale up compute by producing more tokens. Unlike approaches based on chain-of-thought, our approach ...

- Abstract We study a novel language model architecture that is capable of scaling test-time computation by implicitly reasoning in latent space. Our model works by iterating a recurrent block, thereby un-rolling to arbitrary depth at test-time. This stands in contrast to mainstream reasoning models that scale up compute by producing more tokens. Un-like approaches based on chain-of-thought, our ...

- Implicit reasoning brings advantages such as lower generation cost, faster inference, and better alignment with internal computation. Although prior surveys have discussed latent representations in the context of reasoning, a dedicated and mechanism-level examination of how reasoning unfolds internally within LLMs remains absent.

- Its core idea is to perform implicit reasoning in the latent space, replacing explicit textual steps with latent vectors to reduce redundant generation and capture more compact information.

## 3. Hardware-Software Co-Design Integrations (New Pillars)
Based on this research, we propose three new hardware prototypes for Edge NPUs:

### Prototype A: HW-LSR (Hardware Latent Space Router)
- **Target:** Implicit Reasoning in Latent Space.
- **Mechanism:** Instead of generating tokens to DRAM KV Cache, HW-LSR loops the final hidden states back into the input register of the first transformer layer. This creates a purely SRAM-bound recurrent loop, allowing an SLM to "think" for 10 passes without a single external memory fetch.

### Prototype B: HW-TTV (Hardware Test-Time Verifier)
- **Target:** Solving the Verification Gap in Parallel Scaling.
- **Mechanism:** A lightweight dedicated ALU array specifically tuned for Process Reward Models (PRM). While the main Tensor Cores generate multiple reasoning paths, HW-TTV computes reward scores in parallel and prunes low-value branches instantaneously.

### Prototype C: HW-MCTS-SRAM (Hardware Monte Carlo Tree Search Manager)
- **Target:** Search Space Explosion during multi-step reasoning.
- **Mechanism:** MCTS requires maintaining a massive tree of states. HW-MCTS-SRAM implements a hardware hash table inside the NPU memory controller to store tree nodes and UCB (Upper Confidence Bound) scores, eliminating CPU-NPU sync overhead.

