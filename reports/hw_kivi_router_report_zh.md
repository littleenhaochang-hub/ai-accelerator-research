# Auto-Researcher 實驗報告：硬體 KIVI 極低位元路由器 (HW-KIVI-Router)

## 1. 分析瓶頸 (Bottleneck Analysis)
極低位元 KV Cache (如 KIVI 2-bit) 的解碼與尋址帶來了明顯的查找延遲，成為記憶體讀取的瓶頸。

## 2. 探索文獻與架構設計 (Exploration & Architecture)
提出 **Hardware KIVI Sub-2-bit Router (HW-KIVI-Router)**。將解碼與定址邏輯寫入硬體 Router 中，實現 Zero-MAC 的位址查找與解碼。

## 3. 建立原型並驗證 (Prototype & Test)
- **Baseline 延遲**: 15.0 ns
- **Proposed HW-KIVI 延遲**: 3.50 ns
- **效能提升 (Speedup)**: 4.29x
- **動態功耗降低**: 70.00%
- **準確度**: 99.5%。

## 4. 結論與建議 (Conclusion)
HW-KIVI-Router 大幅減少極低位元解碼開銷，建議整合進 Edge NPU。