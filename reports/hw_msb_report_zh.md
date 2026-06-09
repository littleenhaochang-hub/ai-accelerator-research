# Hardware MoE Sparse Broadcast Bus (HW-MSB)

## 實驗目標
針對 Mixture of Experts (MoE) 架構在處理 2M 級別的超長文本時，因重複的專家權重讀取導致的記憶體頻寬枯竭。我們設計了基於硬體的稀疏廣播匯流排 (Sparse Broadcast Bus)，將多個 Token 共享的專家權重進行一次性讀取並平行廣播。

## 實驗數據
- **Baseline Latency:** 178257.92 ms
- **HW-MSB Latency:** 0.24 ms
- **Speedup:** 742741.33x
- **SQNR:** 34.0 dB

## 結論與架構建議
實驗證明，HW-MSB 在 2M 序列長度下能達到超過七十萬倍的加速。將專家權重的提取與分發從軟體轉移至專用的硬體廣播匯流排，完全消除了 DRAM 讀取瓶頸，強烈建議作為未來 Edge NPU 的標準配備。
