# Hardware QK-Norm Fuser (HW-QKNF)
## 針對 Query/Key Normalization 的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
現代架構如 LLaMA-3 常在 Query 與 Key 投影後直接應用 Normalization (RMSNorm) 以穩定訓練。然而在推論階段，軟體 Kernel 必須先將投影結果寫入 SRAM，再啟動另一個 Normalization Kernel 將其讀出、計算變異數並對齊，產生了多餘的 SRAM Read/Write Round-trip，浪費了寶貴的內部頻寬。

### 2. 探索文獻 (Explore)
我們提出 Hardware QK-Norm Fuser (HW-QKNF)。透過在 Tensor Core (執行 Q/K Projection) 的輸出端加入暫存器級別的單階段 RMSNorm 計算單元。讓 Query/Key 向量在產生後，在暫存器內直接完成常規化，再寫入 SRAM。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_qknf_sim.py` 進行 64K Context 模擬驗證：
- **Baseline QK-Norm Latency:** 16004.50 ms
- **HW-QKNF Latency:** 8000.50 ms
- **Speedup (加速比):** 2.00x
- **SRAM 頻寬縮減:** 50.00%

### 4. 結論
實作 HW-QKNF 能夠精確消除 QK-Norm 帶來的中間記憶體傳輸瓶頸。建議將此「暫存器級常規化引擎」整合入下一代 Edge NPU 的 MAC 輸出管線中。
