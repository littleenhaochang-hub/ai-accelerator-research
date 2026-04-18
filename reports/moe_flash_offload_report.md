# MoE Flash Offloading Hardware Architecture 驗證報告

## 執行摘要
在邊緣裝置 (Edge NPU) 執行大型 MoE 模型時，由於 DRAM 容量受限，常需將未活化的專家 (Experts) 卸載至 UFS 4.0 / NVMe 快閃記憶體。本實驗驗證了即時從 Flash 讀取專家的延遲。

## 實驗數據與分析
- **目標模型**: 8x7B MoE (如 Mixtral)，每層啟動 2 個專家，以 4-bit 量化，每層每個專家約 110MB。
- **總數據量**: 單一 token 生成需拉取 7,040 MB 的專家權重。
- **硬體傳輸瓶頸**:
  - UFS 4.0 (4 GB/s): 讀取延遲高達 **1718.75 ms/token** (~0.58 TPS)。
  - LPDDR5 (100 GB/s): 讀取延遲約 **68.75 ms/token** (~14.5 TPS)。

## 硬體架構結論
1. **直接 UFS 讀取不可行**: 完全依賴 UFS 4.0 直接讀取 (Direct Flash Read) 進行 MoE 推論，會導致嚴重的 I/O 瓶頸，TPS < 1。
2. **硬體/軟體協同設計建議**: 邊緣 NPU 必須內建「非對稱預取引擎 (Asynchronous Lookahead Prefetcher)」，利用前幾層的計算時間與推測性預測 (Speculative Routing)，提前從 UFS 將下一層專家載入 DRAM，同時需要配置專屬的 LFU Expert Cache，掩蓋 Flash 讀取延遲。
