# MoE 非同步預取硬體架構 (MoE Asynchronous Prefetching)

## 實驗結果
- 同步載入延遲: 1.9908s
- 非同步預取延遲: 1.4078s
- 加速比: 1.41x

## 結論
透過 DMA 控制器進行硬體層級的 Lookahead Prefetching，我們可以將 PCIe 傳輸延遲與張量核心運算完美重疊，大幅提升 MoE 模型的推理吞吐量。建議將此「硬體非同步預取引擎 (HW-Async-Prefetch Engine)」整合入 NPU 中。