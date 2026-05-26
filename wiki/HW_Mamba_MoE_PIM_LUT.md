# Hardware Mamba-MoE PIM-LUT Router

- **Date**: 2026-05-25
- **Experiment Script**: `mamba_moe_pim_lut_sim.py`
- **Result**: Baseline latency 1096.05 ms, PIM-LUT latency 114.85 ms. Speedup: 9.54x. SQNR: 32.1 dB.
- **Summary**: By migrating Mamba-MoE expert routing to an inline SRAM LUT and Processing-in-Memory, we completely eliminate the CPU-GPU memory transfer bottleneck, maintaining a high SQNR of 32.1 dB.
