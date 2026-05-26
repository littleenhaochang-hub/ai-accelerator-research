# HW-DAS: Hardware DiT Activation Sparsifier

**Goal:** Accelerate Diffusion Transformers (DiT) on edge devices by exploiting spatial-temporal redundancy across diffusion timesteps.
**Method:** Inline hardware predictor to dynamically clock-gate MAC arrays for patches with negligible updates.
**Results:** 2.86x latency speedup and 65.00% dynamic energy reduction.

[Report](../reports/hw_dit_activation_sparsity_report_zh.md)
[Code](../hw_dit_activation_sparsity_sim.py)