# Stochastic Computing Hardware (Sub-1-bit)

**Date:** 2026-04-29
**Context:** Extreme Sub-1-bit Quantization Hardware
**File:** `reports/sc_mac_058bit_report_zh.md`

## Summary
Evaluated Stochastic Computing (SC) for extreme edge devices. By encoding values as probabilities in bitstreams, MAC operations are reduced to simple AND/MUX logic gates. Our simulation (`sc_mac_058bit_sim.py`) demonstrated a **93.10% reduction in dynamic MAC energy** compared to INT4 baselines.

## Hardware Implementation Proposal
Integrate "SC Cores" (Stochastic Computing Cores) utilizing bitstream generators and parallel AND/MUX logic matrices to execute non-critical transformer layers on extreme edge devices (e.g., smartwatches, IoT sensors).
