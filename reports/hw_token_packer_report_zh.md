# Hardware Token Packer 模擬報告

## 摘要
探討針對高度稀疏注意力機制 (Sparse Attention)，將零散的有效 Token 打包的過程由軟體 Gather/Scatter 操作轉為硬體層級的 Token Packer 加速。

## 實驗設計
- 模擬 64K context，稀疏度高達 90%。
- 軟體透過索引收集有效 Token；硬體直接在資料傳輸路徑中動態打包。

## 實驗結果
- **SW Gather/Scatter Latency**: 39.32 s
- **HW Token Packer Latency**: 0.65 s
- **Speedup**: 60.00x

## 架構建議
軟體的記憶體不連續存取 (Gather/Scatter) 在長文本稀疏注意力中會成為致命瓶頸。建議在 Edge NPU 記憶體控制器中實作「Hardware Token Packer」，以確保 MAC 陣列能持續接收連續的有效資料，大幅提升稀疏架構的吞吐量。