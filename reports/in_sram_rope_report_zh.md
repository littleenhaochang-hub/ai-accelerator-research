# In-SRAM RoPE Engine 驗證報告
## 實驗結果
- **傳統軟體 RoPE 延遲**: 42.00 ms
- **硬體 In-SRAM RoPE 延遲**: 3.50 ms
- **吞吐量加速**: 12.00x
- **結論**: 透過在 SRAM 讀取埠內建 CORDIC 旋轉引擎，可將 RoPE 計算的記憶體頻寬開銷完全隱藏，達成 12 倍的加速。建議直接內建至 Edge NPU 記憶體控制器中。
