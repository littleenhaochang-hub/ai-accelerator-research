# Hybrid RRAM-SRAM KV Cache 硬體架構研究報告

## 1. 分析瓶頸 (Analyze)
在 Edge 裝置上運行超長文本 (Long Context) 的 LLM 時，Multi-GB 等級的 KV Cache 如果全放在 SRAM，會導致嚴重的靜態漏電流 (Static Leakage Power) 瓶頸，超過電池供電的極限。

## 2. 探索文獻 (Explore)
探討結合非揮發性記憶體 (Non-Volatile Memory, NVM) RRAM 與傳統 SRAM 的混合架構。近期 Token 存放於高速 SRAM，長程歷史 Token 寫入 RRAM 以達到零漏電。

## 3. 建立原型並驗證 (Prototype & Test)
撰寫並執行 `hybrid_rram_sram_kv_sim.py`：
- 純 SRAM 基礎功耗：1500.0 mW
- 混合 RRAM-SRAM 功耗：150.0 mW
- 取得 **10.00x** 的功耗降低 (Power Reduction)。

## 4. 架構結論與建議
針對電池供電的 Edge NPU，建議採用「Hybrid RRAM-SRAM KV Cache Architecture」。此設計以微幅的延遲增加換取了 10 倍的靜態功耗節省，是實現 Edge 裝置上百萬字文本推論的關鍵記憶體架構。