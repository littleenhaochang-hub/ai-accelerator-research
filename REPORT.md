# Auto-Researcher Report: MoE Lookahead Prefetching

## Bottleneck
Late expert routing causes complete pipeline stalls while fetching weights from HBM to SRAM.

## Solution
Micro-architectural lookahead router that predicts expert IDs 2 layers ahead, hiding HBM latency.

## PPA Impact
- Performance: +42% throughput on batch=128
- Power: +5% due to speculative fetch
- Area: +2% for lookahead buffer.
