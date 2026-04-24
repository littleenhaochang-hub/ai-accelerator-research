# Hardware KV Cache Compressor (硬體 KV 快取壓縮器)

## 實驗背景 (Background)
為了最大化 Edge NPU 內建的 SRAM 效益，通常會將 KV Cache 量化為 INT8 或 INT4。但為了維持精度，必須採用「Outlier-Aware (離群值感知)」的壓縮法：保留少數極端值為 FP16，其餘壓縮為 INT4。在軟體層面進行這種掃描、分離與 Bit-packing，會嚴重消耗記憶體頻寬，導致 Prefill 階段的延遲飆升。

## 物理模擬 (Physical Simulation)
透過 `kv_cache_compressor_hw_sim.py`，比較了軟體壓縮與硬體即時壓縮引擎的效能：
- **軟體 KV 壓縮延遲 (16K Tokens)**: 4194.30 ms
- **硬體 KV 壓縮延遲**: 209.72 ms
- **整體加速比**: 20.00x

## 架構提案 (Architectural Proposal)
提議在 NPU 的 SRAM 寫入路徑上整合 **「Inline Outlier-Aware KV Compressor」**。
當向量資料從運算陣列流出準備寫入 SRAM 時，該硬體單元會即時偵測 Outlier，將其分流至專用的 FP16 緩衝區，並將剩餘資料硬體級 Bit-pack 為 INT4。在讀取時，對應的解壓縮器 (Decompressor) 會在單一週期內無縫還原向量。這讓 Edge 設備能享受極致的記憶體壓縮率，而無須支付昂貴的軟體運算代價。
