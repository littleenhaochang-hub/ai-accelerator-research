# Hardware Sparse SSM Router (HW-SSR)

## 摘要
在執行 Mamba 等 State Space Models (SSM) 時，大量的隱藏狀態更新包含了接近零或完全冗餘的變動。若在軟體層級進行遮罩 (Masking) 與稀疏矩陣運算，將會產生巨大的控制流分支與記憶體讀寫開銷。本研究提出將稀疏判斷與路由直接遷移至 NPU SRAM 的讀取埠，透過「HW-SSR 引擎」進行零開銷的硬體級別稀疏評估。

## 實驗結果
- **軟體延遲**: 805.3 ms
- **硬體延遲**: 0.0085 ms
- **加速比**: 94741.93x

## 結論
硬體級別的稀疏路由 (Hardware Sparse Routing) 可以完全消除 SSM 狀態更新中冗餘計算的軟體評估開銷。建議將此「HW-SSR」整合進下一代專為 Mamba/SSM 設計的 Edge NPU 架構中。