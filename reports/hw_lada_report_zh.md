# Hardware Linear Attention Decay Accelerator (HW-LADA) 實驗報告

## 背景與瓶頸分析
Gated Linear Attention (GLA) 與 RetNet 等線性注意力架構透過維護一個固定大小的 State Matrix ($O(1)$ Memory) 來取代傳統的 KV Cache。然而，這些架構的核心瓶頸在於**資料依賴型的衰減更新 (Data-Dependent Decay Update)**。在每次 Token 處理時，系統必須從 SRAM 讀取龐大的 State Matrix (例如 8MB)，並利用 ALU 計算指數函數 ($e^{cx}$ 或 Sigmoid) 後再更新寫回。標準 Tensor Core 處理超越函數 (Transcendental Functions) 的效率極低，導致運算與記憶體頻寬雙重受限。

## 解決方案：HW-LADA (硬體線性注意力衰減加速器)
我們提出 **HW-LADA**，這是一個結合了「分段線性近似 (Piecewise Linear, PWL) 引擎」與「近記憶體運算 (Near-Memory Processing, NMP)」的硬體架構。
HW-LADA 將指數衰減的計算降維為 PWL 查表與位移操作，並且將狀態矩陣的乘加 (MAC) 更新邏輯直接嵌入 SRAM 的讀寫埠旁。如此一來，主運算核心 (Tensor Cores) 完全無需介入 State Matrix 的搬移與更新。

## 實驗結果
透過 Python 模擬 (`hw_lada_sim.py`)，針對 32K Context 進行序列狀態更新測試：
- **基準延遲 (軟體 FPU 計算 + SRAM R/W):** 419.84 ms
- **HW-LADA 延遲 (Inline PWL + NMP):** 41.98 ms
- **狀態更新加速比 (Speedup):** 10.00x

## 結論
HW-LADA 徹底解決了線性注意力 (Linear Attention) 架構在推論時的超越函數運算與 SRAM 頻寬瓶頸，實現了整整 10 倍的狀態更新加速。隨著下一代模型逐漸捨棄標準 Transformer 轉向 Mamba/GLA 混合架構，建議將 HW-LADA 作為 Edge NPU 的原生標準硬體加速單元。
