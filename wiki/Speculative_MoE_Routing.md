# Speculative MoE Routing Hardware

透過上一層的 Activation 提前預測未來的 Expert IDs，並利用非同步 DMA (Asynchronous TMA) 預取權重。此方法可將 PCIe 與記憶體傳輸延遲與運算重疊。

- **Latency Baseline:** 2.45 ms / token (Demand Fetching)
- **Speedup:** 10.00x
- **Hardware Integration:** DMA 控制器內建輕量級 MoE 預測器 (Lookahead Predictor)。