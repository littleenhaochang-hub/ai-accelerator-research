# MoE PIM Prefetching Simulation Report
## 問題 (Problem)
MoE decoding 過程中的 CPU-GPU 記憶體傳輸是主要的瓶頸，因為 Experts 的參數龐大且 PCIe 頻寬有限。

## 模擬 (Simulation)
- Experts 數量: 128
- Hidden Dimension: 4096
- 單一 Expert 大小: 32.00 MB
- PCIe Gen4 頻寬: 32 GB/s
- 提議的 PIM 頻寬: 64 GB/s

## 結果 (Results)
- 標準傳輸時間 (每個 Expert): 0.9766 ms
- PIM 傳輸時間 (每個 Expert): 0.4883 ms
- 加速比: 2.00x
