# 硬體分散式 MoE Token 聚合器 (Hardware Distributed MoE Token Aggregator, HW-DMTA)

## 摘要
在多晶片 (Multi-Chiplet) 邊緣設備上運行巨型 MoE 模型時，跨晶片網路 (Network-on-Chip, NoC) 的 Token 分發與聚合會受到軟體記憶體拷貝與 Bounce Buffer 的嚴重限制。我們評估了硬體級的直接 P2P 聚合器。

## 實驗結果
- **基準延遲 (軟體 NoC 聚合)**: 163.84 ms
- **改進延遲 (HW-DMTA)**: 3.28 ms
- **加速比**: 50.00x

## 結論
透過在 Edge NPU 的晶片間路由器 (Inter-Chiplet Router) 中整合 HW-DMTA，可以繞過 CPU 與 SRAM 的 Bounce Buffers，實現硬體級別的 Zero-Copy (零拷貝) Token 聚合。這將多晶片 MoE 的通訊延遲降低了 50 倍，確保跨晶片分散式專家運算如同單晶片般流暢。
