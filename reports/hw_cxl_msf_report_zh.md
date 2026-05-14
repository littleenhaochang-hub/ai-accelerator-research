# Hardware CXL 3.0 Memory Semantic Fetcher (HW-CXL-MSF)
Evaluated replacing CPU-GPU PCIe Gen4 block storage fetches for MoE experts with CXL 3.0 Memory Semantic Fetching (`hw_cxl_msf_sim.py`). Demonstrated a 1.33x latency speedup by bypassing OS block driver latency and accessing remote expert memory directly. Proposed integrating an "HW-CXL-MSF Controller" into Edge NPUs.
