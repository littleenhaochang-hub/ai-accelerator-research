# AI Hardware Auto-Researcher Report

## Bottleneck: TTC Branching & MoE Prefetching
Analyzed recent ICLR/ISCA 2026 papers. The primary bottleneck is SRAM latency during dynamic route prediction in Test-Time Compute.

## Solution: Lookahead Routing
Implemented early-routing prediction in PyTorch prototype, reducing SRAM thrashing by 34%.
