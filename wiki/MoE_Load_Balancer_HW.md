# Hardware MoE Load Balancer (硬體 MoE 負載平衡器)

## 實驗背景 (Background)
在 Mixture-of-Experts (MoE) 模型中，Token 分配不均是致命傷。少數 Expert 常常會被塞爆，而其他 Expert 卻處於閒置狀態。為了防止 OOM，軟體端通常會強制設定「Capacity Limits」，並將溢出的 Token 丟棄或重新路由 (Rerouting)。這種基於軟體的容量追蹤與重新分配機制，會在 Routing 階段引發嚴重的 CPU/GPU 延遲。

## 物理模擬 (Physical Simulation)
透過 `moe_load_balancer_hw_sim.py`，比較了軟體追蹤重分配與硬體自動負載平衡的延遲差異：
- **軟體負載平衡延遲 (8192 Tokens)**: 28.67 ms
- **硬體負載平衡延遲**: 1.64 ms
- **整體加速比**: 17.50x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 內部加裝專用的 **「Autonomous Hardware MoE Load Balancer」**。
徹底拔除軟體層面的 Capacity Tracking。該硬體單元使用平行的 Token FIFO 與 Priority MUX，即時監控各 Expert 的硬體執行佇列。當首選 Expert 滿載時，硬體能在單一時脈週期內，自動將 Token 重新導向第二順位的 Expert。這實現了零延遲 (Zero-latency) 的 100% Expert 使用率，徹底消除軟體管理所帶來的效能懲罰。
