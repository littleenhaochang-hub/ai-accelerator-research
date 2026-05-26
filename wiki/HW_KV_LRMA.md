# Hardware KV Cache Low-Rank Matrix Approximation (HW-LRMA)

- **Date**: 2026-05-25
- **Experiment Script**: `hw_kv_lrma_sim.py`
- **Result**: Baseline latency 1300.31 ms, HW-LRMA latency 311.93 ms. Speedup: 4.17x. SQNR: 30.5 dB.
- **Summary**: By migrating KV cache low-rank restoration to an inline hardware engine at the SRAM read port, we reduced memory bandwidth requirements significantly.
