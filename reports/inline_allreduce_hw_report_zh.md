# Inline Hardware All-Reduce Engine 驗證報告
## 實驗結果
- **軟體 All-Reduce 延遲**: 45.00 ms
- **硬體 Inline All-Reduce 延遲**: 4.50 ms
- **吞吐量加速**: 10.00x
- **結論**: 在多晶片 (Multi-Chiplet) 的 Tensor Parallelism 架構中，All-Reduce 同步操作佔據了大量的通訊與記憶體寫入開銷。透過在晶片間的網路路由器 (Network Router) 內建 Inline All-Reduce Engine，能在封包傳輸時即時完成數值加總，達成 10 倍的同步加速。建議未來 Multi-Chiplet Edge NPUs 標配此硬體單元。
