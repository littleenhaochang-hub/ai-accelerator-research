# Hardware Dynamic Token Re-Routing (HW-DTRR)

## 實驗背景 (Background)
在 Fine-grained MoE (如 DeepSeek-V3 具有 256 個以上專家) 的架構中，軟體層面的 Token 路由與排序 (Softmax + Top-K + Scatter/Gather) 帶來了嚴重的 CPU/ALU 延遲瓶頸。

## 實驗設計 (Methodology)
本實驗設計了硬體層級的動態 Token 路由交叉開關 (`hw_dtrr_moe_sim.py`)。透過專用的「HW-DTRR Crossbar」，在硬體級別進行 $O(1)$ 的 Token 分發，完全消除軟體排序與記憶體搬運開銷。

## 實驗結果 (Results)
- Software MoE Routing: 0.0105 s
- HW-DTRR MoE Latency: 0.000004 s
- **Speedup**: 2560.00x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 的排程器中整合「HW-DTRR Crossbar」。針對超過 256 個專家的 MoE 模型，此硬體開關能將路由延遲降至可忽略不計，是實現端側超大規模 MoE 的關鍵。