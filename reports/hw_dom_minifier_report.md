# Hardware DOM Minifier Engine for Edge Agentic AI

## Background
According to our Edge Agentic AI roadmap, passing full un-truncated raw DOM snapshots (e.g., 2MB of HTML/CSS/JS) into local LLMs results in severe Context OOM and Prefill latency degradation. CPU-bound minification using regex or libraries like BeautifulSoup introduces a massive ~1 second latency bottleneck per turn before the LLM even begins processing.

## Hardware Simulation
We simulated the latency of standard CPU DOM parsing versus a dedicated Hardware Finite State Machine (FSM) DOM Minifier (`hw_dom_minifier_sim.py`) capable of stripping CSS/scripts and converting HTML to accessibility trees at memory bandwidth speeds.
- **CPU Software Latency:** 1024.00 ms (for a 2MB DOM)
- **Hardware FSM Latency:** 30.72 ms
- **Speedup:** 33.33x

## Architectural Proposal
We propose integrating a **"Hardware DOM Minifier Engine"** at the NPU ingress bus. As the DMA fetches the raw DOM text from system memory, this inline FSM strips non-semantic tags (scripts, styles, SVGs) and dynamically truncates the tree, streaming a compressed, LLM-ready representation directly into the NPU SRAM. This completely bypasses the CPU bottleneck for Agentic AI workflows, maintaining real-time responsiveness for local browser agents.
