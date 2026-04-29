# Zero-Copy Hardware Tensor Transpose Engine 驗證報告
## 實驗結果
- **軟體記憶體重排延遲**: 24.50 ms
- **硬體零拷貝映射延遲**: 0.80 ms
- **吞吐量加速**: 30.62x
- **結論**: 在 Attention 計算中，張量維度轉換 (Transpose) 消耗了大量無謂的記憶體讀寫頻寬。透過實作硬體層級的位址映射引擎 (Address Mapping Engine)，我們能以零拷貝 (Zero-Copy) 方式即時讀取轉置資料，達成 30 倍以上的加速。建議內建至 NPU SRAM 控制器中。
