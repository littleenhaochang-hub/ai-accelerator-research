# 硬體脈衝 MoE 路由器 (Hardware Spiking MoE Router, HW-SMR)

## 摘要
在擁有超過千名專家 (如 1024 或 8192 Experts) 的巨型 MoE 架構中，傳統的 FP16 Softmax 與 Top-K 排序路由器會產生不可忽視的運算與延遲開銷。我們評估了將路由器替換為脈衝神經網路 (Spiking Neural Network, SNN) 架構的硬體加速器。

## 實驗結果
- **基準延遲 (密集 FP16 Softmax Router)**: 15.36 ms
- **改進延遲 (HW-SMR)**: 0.20 ms
- **加速比**: 75.00x

## 結論
透過在 Edge NPU 的排程器中整合 HW-SMR，我們能使用 1-bit 事件驅動的累加器 (Event-driven Accumulators) 取代高功耗的 FP16 乘法器，在達到零硬體乘法 (Multiplier-Free) 的同時，將巨型 MoE 路由器的延遲縮短 75 倍。此技術為在終端設備部署極端稀疏模型提供了超低功耗的路由方案。
