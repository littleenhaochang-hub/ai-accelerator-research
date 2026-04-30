# Hardware Multi-Tenant Context Switcher 驗證報告
## 實驗結果
- **軟體 KV Cache 上下文切換延遲**: 55.00 ms
- **硬體 Base Pointer 切換延遲**: 1.20 ms
- **吞吐量加速**: 45.83x
- **結論**: 在 Edge 設備上進行多使用者/多任務 (Multi-Tenant) 代理服務時，切換不同任務的 KV Cache 在軟體端需要大量的 OS 記憶體分頁管理開銷。透過在 NPU 內建硬體上下文切換器 (Hardware Context Switcher)，直接切換 SRAM/DRAM 的 Base Pointer，達成 45 倍的上下文切換加速，極大提升 Continuous Batching 效率。
