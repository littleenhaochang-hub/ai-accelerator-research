# Jamba (MoE-Mamba Hybrid) Hardware Acceleration

在探索 Mamba (SSM) 與 MoE 結合的混合架構 (如 Jamba) 時，系統會面臨 DRAM 提取專家權重的瓶頸，以及 Mamba 序列掃描的運算瓶頸。

## 架構提案：Asynchronous Jamba DMA & Scan Scheduler
為徹底解決這兩個瓶頸，我們設計了非同步排程器，讓硬體能夠同時處理：
1. **MoE Lookahead Prefetching：** 利用 DMA 在背景將 N+1 層的專家權重搬入 SRAM。
2. **Associative Scan ALU Trees：** 將 O(N) 的 Mamba State 掃描平行化為 O(log N)。

## 實測數據
根據 `jamba_hardware_sim.py` 的模擬，此硬體軟體協同設計能將硬體執行時間從 1022.41 ms 壓縮至 367.58 ms，達成 **2.78x** 的吞吐量加速。此設計已被納入 OpenClaw Edge NPU 的下一代架構藍圖中。