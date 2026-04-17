# Continuous Batching Hardware Scheduler

## 實驗背景
在處理多個長度不一的 Requests 時，Static Batching 會因為長度對齊 (Padding) 而產生大量硬體閒置。Continuous Batching 能以 Token 為單位動態插入新 Request。

## 硬體模擬與分析
- **腳本**: `continuous_batching_sim.py`
- 在長度差異極大 (100~1000) 的分佈下，Continuous Batching 能將硬體利用率極大化，達成 **1.95x** 的吞吐量加速。

## 架構協同設計結論
Edge AI 伺服器/晶片應引入 **Hardware Context Switcher**，將 OS 層級的 Batch 排程下放至 NPU 硬體層。這能達到 Zero-Cycle Context Switch，確保 Tensor Core 不會因為軟體層級的 Python overhead 而產生氣泡。
