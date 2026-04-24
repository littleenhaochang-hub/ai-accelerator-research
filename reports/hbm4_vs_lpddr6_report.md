# Edge NPU 記憶體技術路線：HBM4 與 LPDDR6 比較分析

## 1. 瓶頸分析 (Bottleneck Analysis)
隨著終端裝置的模型突破 30B 參數，記憶體頻寬成為解碼階段的絕對瓶頸。業界開始討論是否應將伺服器級的 HBM (High Bandwidth Memory) 下放至行動與邊緣裝置。我們針對 HBM4 與 LPDDR6 在 35B 模型 (INT4, 17.5GB) 的情境下進行了 PPA (Power, Performance, Area/Cost) 模擬。

## 2. 探索與模擬驗證 (Exploration & Test)
執行實驗腳本：`hbm4_vs_lpddr6_sim.py`
- **LPDDR6**: 
  - 頻寬: 100 GB/s 
  - Token 生成速度 (TPS): 5.71 TPS
  - 記憶體讀取絕對功耗: 2.80W
  - 封裝成本: 1.0x (標準 PCB)
- **HBM4**: 
  - 頻寬: 2000 GB/s
  - Token 生成速度 (TPS): 114.29 TPS
  - 記憶體讀取絕對功耗: 12.80W
  - 封裝成本: 25.0x (需 Silicon Interposer / 2.5D 封裝)

## 3. 結論與硬體架構建議
儘管 HBM4 的每位元傳輸能耗 (pJ/bit) 較低，能提供 20 倍的解碼速度，但在全速運行下，單純記憶體的絕對功耗即高達 12.8W，完全超出無風扇或電池供電設備的散熱極限。此外，高昂的 2.5D 封裝成本也抹殺了消費級量產的可行性。
**架構決策：** 邊緣裝置必須堅守 LPDDR 路線。為了解決 LPDDR6 僅 5.7 TPS 的頻寬困境，我們不能依賴升級記憶體硬體，而必須透過「Sub-2-bit 極端量化 (如 BitNet)」與「投機解碼 (Speculative Decoding)」來從演算法端突圍。
