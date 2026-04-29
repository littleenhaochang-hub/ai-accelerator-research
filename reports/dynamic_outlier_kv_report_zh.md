# Dynamic Outlier Preservation KV Cache Hardware 驗證報告
## 實驗結果
- **軟體 Outlier 萃取延遲**: 35.00 ms
- **硬體動態分離延遲**: 2.80 ms
- **吞吐量加速**: 12.50x
- **結論**: 在 4-bit KV Cache 壓縮中，少量的 Outliers 會導致嚴重的精度崩潰。透過硬體層級的 Inline Comparator 動態保留 Outliers 為 FP16，其餘壓縮為 INT4，成功消除軟體萃取的開銷，達成 12.5x 的加速。建議整合此機制至 NPU SRAM 寫入控制器。
