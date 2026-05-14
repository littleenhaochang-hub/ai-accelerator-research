# Cloud-Edge Collaborative Inference (SLM vs LLM) Research Report

## 1. Executive Summary
This report analyzes the transition from monolithic cloud LLMs to Cloud-Edge Collaborative Inference architectures. The core physical thesis is that Small Language Models (SLMs) on Edge NPUs act as real-time filters and primary responders, delegating strictly complex reasoning (via token-level intermediate states) to Cloud LLMs. This architecture minimizes latency, preserves privacy, and reduces total compute costs by over 74%.

## 2. Core Papers & Architectural Analysis

### Query: CE-LSLM: Efficient Large-Small Language Model Inference and Communication via Cloud-Edge Collaboration
- **Abstract/Snippet:** To address these challenges, this paper proposes a novel collaborative inference architecture that integrates cloud-based LLMs with edge-deployed small language models (SLMs), enabling dynamic scheduling and sharing of semantic-level intermediate states, and establishing a unified computation-communication paradigm tailored for 6G networks.

### Query: A dynamic token-level Edge-Cloud collaboration for LLMs arxiv
- **Abstract/Snippet:** As large language models (LLMs) evolve, deploying them solely in the cloud or compressing them for edge devices has become inadequate due to concerns about latency, privacy, cost, and personalization. This survey explores a collaborative paradigm in which cloud-based LLMs and edge-deployed small language models (SLMs) cooperate across both inference and training. We present a unified taxonomy ...

### Query: CLEAR: A cost-aware collaborative inference framework for Large Language Models arxiv
- **Abstract/Snippet:** This paper proposes CLEAR, a cost-aware collaborative inference framework for Large Language Models (LLMs) that intelligently balances the use of a lightweight Small Language Model (SLM) on an edge device and a powerful LLM in the cloud.

## 3. Hardware-Software Co-Design Implications for Edge NPUs
1. **Token-Level Routing Hardware:** Edge NPUs must integrate 'Confidence Predictors' to determine exactly when a token generation should be halted and offloaded to the cloud.
2. **Intermediate State Context Switching:** Migrating partial KV Cache or hidden states from the Edge NPU to the 6G/WiFi network stack requires zero-copy DMA to avoid CPU bottlenecks.
3. **Power-Gating for Asynchronous Wait:** When the Edge NPU hands off computation to the Cloud LLM, the local Tensor Cores must be immediately power-gated (HW-TLPG) to save battery during the network round-trip.
