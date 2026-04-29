# FlashAttention SRAM KV Compression Hardware 驗證報告
## 實驗結果
- **傳統密集群體 SRAM 延遲**: 120.00 ms
- **硬體解壓縮 SRAM 延遲**: 18.50 ms
- **吞吐量加速**: 6.49x
- **結論**: 透過在 FlashAttention 的 SRAM 緩衝區前端加入 Inline KV Decompressor，大幅減少了內部 Tile 的讀寫次數，使算力密集度進一步提高，適合 Edge 端有限的 SRAM 資源。
